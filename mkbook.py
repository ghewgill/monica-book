from __future__ import print_function

import os
import sqlite3

try:
    os.unlink("monica.db")
except OSError:
    pass

db = sqlite3.connect("monica.db")

db.execute("""
    CREATE TABLE activities(
        id number,
        account_id number,
        activity_type_id number,
        summary string,
        description string,
        date_it_happened datetime,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE activity_contact(
        activity_id number,
        contact_id number,
        account_id number
    )
""")

db.execute("""
    CREATE TABLE activity_statistics(
        id number,
        account_id number,
        contact_id number,
        year number,
        count number,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE addresses(
        id number,
        account_id number,
        contact_id number,
        name string,
        street string,
        city string,
        province string,
        postal_code string,
        country_id number,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE calls(
        id number,
        account_id number,
        contact_id number,
        called_at datetime,
        content string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE contact_field_types(
        id number,
        account_id number,
        name string,
        fontawesome_icon string,
        protocol string,
        delible number,
        type string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE contact_fields(
        id number,
        account_id number,
        contact_id number,
        contact_field_type_id number,
        data string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE contact_tag(
        contact_id number,
        tag_id number,
        account_id number,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE contacts(
        id number,
        account_id number,
        first_name string,
        middle_name string,
        last_name string,
        surname string,
        gender string,
        is_partial boolean,
        is_dead boolean,
        deceased_special_date_id number,
        last_talked_to datetime,
        birthday_special_date_id number,
        first_met_through_contact_id number,
        first_met_special_date_id number,
        first_met_where string,
        first_met_additional_info string,
        job string,
        company string,
        food_preferencies string,
        has_avatar boolean,
        avatar_external_url string,
        avatar_file_name string,
        avatar_location string,
        gravatar_url string,
        linkedin_profile_url string,
        last_consulted_at datetime,
        created_at datetime,
        updated_at datetime,
        default_avatar_color string,
        has_avatar_bool boolean
    )
""")

db.execute("""
    CREATE TABLE debts(
        id number,
        account_id number,
        contact_id number,
        in_debt boolean,
        status string,
        amount number,
        reason string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE events(
        id number,
        account_id number,
        contact_id number,
        object_type string,
        object_id number,
        nature_of_operation string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE journal_entries(
        id number,
        account_id number,
        date datetime,
        journalable_id number,
        journalable_type string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE notes(
        id number,
        account_id number,
        contact_id number,
        body string,
        is_favorited boolean,
        favorited_at datetime,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE offsprings(
        id number,
        account_id number,
        contact_id number,
        is_the_child_of number,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE relationships(
        id number,
        account_id number,
        contact_id number,
        with_contact_id number,
        anniversary string,
        is_active boolean,
        breakup_reason string,
        created_at string,
        updated_at string
    )
""")

db.execute("""
    CREATE TABLE reminders(
        id number,
        account_id number,
        contact_id number,
        special_date_id number,
        title string,
        description string,
        frequency_type string,
        frequency_number number,
        last_triggered datetime,
        next_expected_date datetime,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE special_dates(
        id number,
        account_id number,
        contact_id number,
        is_age_based boolean,
        is_year_unknown boolean,
        date datetime,
        reminder_id number,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE tags(
        id number,
        account_id number,
        name string,
        name_slug string,
        description string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE users(
        id number,
        first_name string,
        last_name string,
        email string, 
        password string,
        remember_token string,
        google2fa_secret string,
        account_id number,
        timezone string,
        currency_id number,
        locale string,
        metric boolean,
        fluid_container boolean,
        contacts_sort_order string,
        name_order string,
        invited_by_user_id number,
        dashboard_active_tab string,
        created_at datetime,
        updated_at datetime
    )
""")

db.execute("""
    CREATE TABLE accounts(
        account_id number,
        token string,
        unknown string
    )
""")

for s in open("monica.sql"):
    s = s.strip()
    if s.startswith("#"):
        continue
    s = s.replace("\\'", "''")
    db.execute(s)

db.commit()

c = db.cursor()
for r in c.execute("SELECT first_name, last_name FROM contacts ORDER BY first_name"):
    print(r[0], r[1])
