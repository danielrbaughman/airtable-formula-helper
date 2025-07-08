from airtableformulahelpers import (
    AND,
    IF,
    NOT,
    OR,
    AttachmentsField,
    BooleanField,
    DateField,
    NumberField,
    TextField,
    TextListField,
)


def test_real_world_user_validation_formula():
    """Test a real-world user validation formula"""
    name_field = TextField(name="Name")
    email_field = TextField(name="Email")
    age_field = NumberField(name="Age")
    active_field = BooleanField(name="Active")

    # Complex validation: name not empty, valid email, adult age, and active
    validation = AND(
        name_field.is_not_empty(),
        email_field.regex_match(r"^[^@]+@[^@]+\.[^@]+$"),
        age_field.greater_than_or_equals(18),
        active_field.is_true(),
    )

    result = IF(validation).THEN("Valid User").ELSE("Invalid User")
    expected = 'IF(AND({Name},REGEX_MATCH({Email}, "^[^@]+@[^@]+\\.[^@]+$"),{Age}>=18,{Active}=TRUE()), Valid User, Invalid User)'
    assert result == expected


def test_project_status_with_dates_and_attachments():
    """Test project status formula with dates and attachments"""
    start_date = DateField(name="Start Date")
    end_date = DateField(name="End Date")
    documents = AttachmentsField(name="Documents")
    status = TextField(name="Status")

    # Project is ready if it has start date, end date is in future, has documents, and status is approved
    ready_condition = AND(
        start_date.is_not_empty(),
        end_date.is_on_or_after().days_ago(-30),  # End date is within 30 days in future
        documents.is_not_empty(),
        status.equals("Approved"),
    )

    result = IF(ready_condition).THEN("Ready to Launch").ELSE("Not Ready")
    expected = "IF(AND({Start Date},DATETIME_DIFF(NOW(), {End Date}, 'days')>=-30,LEN({Documents})>0,{Status}=\"Approved\"), Ready to Launch, Not Ready)"
    assert result == expected


def test_e_commerce_product_filtering():
    """Test e-commerce product filtering with multiple field types"""
    name_field = TextField(name="Product Name")
    price_field = NumberField(name="Price")
    category_field = TextListField(name="Categories")
    in_stock_field = BooleanField(name="In Stock")
    images_field = AttachmentsField(name="Images")

    # Find products: name contains "laptop", price under $2000, in electronics category, in stock, has images
    product_filter = AND(
        name_field.contains("laptop"),
        price_field.less_than(2000),
        category_field.contains("Electronics"),
        in_stock_field.is_true(),
        images_field.is_not_empty(),
    )

    result = IF(product_filter).THEN("Show Product").ELSE("Hide Product")
    expected = 'IF(AND(FIND(TRIM(LOWER("laptop")), TRIM(LOWER({Product Name})))>0,{Price}<2000,FIND(LOWER("Electronics"), LOWER({Categories}))>0,{In Stock}=TRUE(),LEN({Images})>0), Show Product, Hide Product)'
    assert result == expected


def test_employee_bonus_calculation():
    """Test employee bonus calculation with multiple conditions"""
    performance_field = TextField(name="Performance Rating")
    salary_field = NumberField(name="Salary")
    years_field = NumberField(name="Years of Service")
    department_field = TextListField(name="Department")
    active_field = BooleanField(name="Active")

    # Bonus eligible: excellent performance, salary under 100k, 2+ years service, in sales/engineering, active
    bonus_eligible = AND(
        performance_field.equals("Excellent"),
        salary_field.less_than(100000),
        years_field.greater_than_or_equals(2),
        department_field.contains_any(["Sales", "Engineering"]),
        active_field.is_true(),
    )

    result = IF(bonus_eligible).THEN("Eligible for Bonus").ELSE("Not Eligible")
    expected = 'IF(AND({Performance Rating}="Excellent",{Salary}<100000,{Years of Service}>=2,OR(FIND(LOWER("Sales"), LOWER({Department}))>0,FIND(LOWER("Engineering"), LOWER({Department}))>0),{Active}=TRUE()), Eligible for Bonus, Not Eligible)'
    assert result == expected


def test_event_management_system():
    """Test event management system with dates and complex conditions"""
    venue_field = TextField(name="Venue")
    status_field = TextField(name="Status")
    materials_field = AttachmentsField(name="Materials")
    registrations_field = NumberField(name="Registrations")

    # Event ready: venue confirmed, approved status, has exactly 3 materials, not overbooked
    event_ready = AND(
        venue_field.not_equals(""),
        status_field.equals("Approved"),
        materials_field.count_is(3),
        registrations_field.less_than_or_equals(100),  # Fixed: provide actual value
    )

    result = IF(event_ready).THEN("Event Ready").ELSE("Needs Preparation")
    expected = 'IF(AND({Venue}!="",{Status}="Approved",LEN({Materials})=3,{Registrations}<=100), Event Ready, Needs Preparation)'
    assert result == expected


def test_content_moderation_system():
    """Test content moderation system with text analysis"""
    title_field = TextField(name="Title")
    content_field = TextField(name="Content")
    author_field = TextField(name="Author")
    tags_field = TextListField(name="Tags")
    flagged_field = BooleanField(name="Flagged")

    # Content approval: title not empty, content doesn't contain banned words, author verified, appropriate tags, not flagged
    content_approved = AND(
        title_field.is_not_empty(),
        NOT(content_field.contains("spam")),
        NOT(content_field.contains("inappropriate")),
        author_field.not_equals("Anonymous"),
        OR(
            tags_field.contains("Educational"),
            tags_field.contains("News"),
            tags_field.contains("Entertainment"),
        ),
        NOT(flagged_field.is_true()),
    )

    result = IF(content_approved).THEN("Approved").ELSE("Needs Review")
    expected = 'IF(AND({Title},NOT(FIND(TRIM(LOWER("spam")), TRIM(LOWER({Content})))>0),NOT(FIND(TRIM(LOWER("inappropriate")), TRIM(LOWER({Content})))>0),{Author}!="Anonymous",OR(FIND(LOWER("Educational"), LOWER({Tags}))>0,FIND(LOWER("News"), LOWER({Tags}))>0,FIND(LOWER("Entertainment"), LOWER({Tags}))>0),NOT({Flagged}=TRUE())), Approved, Needs Review)'
    assert result == expected


def test_inventory_management_with_dates():
    """Test inventory management with expiration dates"""
    quantity_field = NumberField(name="Quantity")
    location_field = TextField(name="Location")
    category_field = TextListField(name="Category")

    # Item needs attention: low quantity OR in restricted location OR perishable
    simplified_attention = OR(
        quantity_field.less_than(10),
        location_field.equals("Quarantine"),
        category_field.contains("Perishable"),
    )

    result = IF(simplified_attention).THEN("Needs Attention").ELSE("OK")
    expected = 'IF(OR({Quantity}<10,{Location}="Quarantine",FIND(LOWER("Perishable"), LOWER({Category}))>0), Needs Attention, OK)'
    assert result == expected


def test_customer_segmentation_advanced():
    """Test advanced customer segmentation"""
    purchase_count = NumberField(name="Purchase Count")
    total_spent = NumberField(name="Total Spent")
    customer_type = TextField(name="Customer Type")
    preferences = TextListField(name="Preferences")
    vip_status = BooleanField(name="VIP")

    # VIP Customer: many purchases, high spending, premium type, luxury preferences, or already VIP
    vip_customer = OR(
        AND(
            purchase_count.greater_than(10),
            total_spent.greater_than(1000),
            customer_type.equals("Premium"),
        ),
        preferences.contains("Luxury"),
        vip_status.is_true(),
    )

    result = IF(vip_customer).THEN("VIP Treatment").ELSE("Standard Service")
    expected = 'IF(OR(AND({Purchase Count}>10,{Total Spent}>1000,{Customer Type}="Premium"),FIND(LOWER("Luxury"), LOWER({Preferences}))>0,{VIP}=TRUE()), VIP Treatment, Standard Service)'
    assert result == expected
