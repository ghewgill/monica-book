from __future__ import print_function

import os
import shutil
import sqlite3

Country = {
    1: "United States",
    2: "Canada",
    159: "Poland",
    210: "Australia",
    218: "New Zealand",
}

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


try:
    shutil.rmtree("epub")
except OSError:
    pass
os.mkdir("epub")

with open("epub/mimetype", "w") as out:
    print("application/epub+zip", file=out)

c = db.cursor()
for contact in c.execute("SELECT id, first_name, last_name FROM contacts WHERE NOT is_partial ORDER BY first_name"):
    with open(os.path.join("epub", "-".join([contact[1], contact[2]]).lower()+".xhtml"), "w") as out:
        print('<?xml version="1.0" encoding="utf-8"?>', file=out)
        print('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">', file=out)
        print('<head>', file=out)
        print('  <title>{} {}</title>'.format(contact[1], contact[2]), file=out)
        print('</head>', file=out)
        print('<body>', file=out)
        print('<h1>{} {}</h1>'.format(contact[1], contact[2]), file=out)
        c2 = db.cursor()
        for address in c2.execute("SELECT street, city, province, postal_code, country_id FROM addresses WHERE contact_id = ?", (contact[0],)):
            print('<p>', file=out)
            if address[0]: print('{}<br />'.format(address[0]), file=out)
            if address[1]: print('{}<br />'.format(address[1]), file=out)
            if address[2]: print('{}<br />'.format(address[2]), file=out)
            if address[3]: print('{}<br />'.format(address[3]), file=out)
            if address[4]: print('{}<br />'.format(Country.get(address[4], address[4])), file=out)
            print('</p>', file=out)
        for contact in c2.execute("SELECT name, data FROM contact_fields, contact_field_types WHERE contact_id = ? AND contact_field_type_id = contact_field_types.id", (contact[0],)):
            scheme = {
                "Email": "mailto:",
                "Phone": "tel:",
            }
            print('<p>{}: <a href="{}{}">{}</a></p>'.format(contact[0], scheme.get(contact[0], ""), contact[1], contact[1]), file=out)
        print('</body>', file=out)
        print('</html>', file=out)

with open("epub/titlepage.xhtml", "w") as out:
    print('<?xml version="1.0" encoding="utf-8"?>', file=out)
    print('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">', file=out)
    print('<head>', file=out)
    print('<title>Cover</title>', file=out)
    print('<style type="text/css" title="override_css">', file=out)
    print('@page {padding: 0pt; margin:0pt}', file=out)
    print('body { text-align: center; padding:0pt; margin: 0pt; }', file=out)
    print('</style>', file=out)
    print('</head>', file=out)
    print('<body>', file=out)
    print('<div>', file=out)
    name = c.execute("SELECT first_name, last_name FROM users").next()
    print('Contact Database for {} {}'.format(*name), file=out)
    print('</div>', file=out)
    print('</body></html>', file=out)

with open("epub/toc.ncx", "w") as out:
    print('<?xml version="1.0" encoding="utf-8"?>', file=out)
    print('<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng">', file=out)
    print('<head>', file=out)
    #print('<meta content="0c159d12-f5fe-4323-8194-f5c652b89f5c" name="dtb:uid"/>', file=out)
    #print('<meta content="2" name="dtb:depth"/>', file=out)
    #print('<meta content="calibre (0.8.68)" name="dtb:generator"/>', file=out)
    #print('<meta content="0" name="dtb:totalPageCount"/>', file=out)
    #print('<meta content="0" name="dtb:maxPageNumber"/>', file=out)
    print('</head>', file=out)
    print('<docTitle>', file=out)
    print('<text>Monica Database</text>', file=out)
    print('</docTitle>', file=out)
    print('<navMap>', file=out)
    for i, r in enumerate(c.execute("SELECT first_name, last_name FROM contacts WHERE NOT is_partial ORDER BY first_name")):
        print('<navPoint id="a{i}" playOrder="{i}">'.format(i=i), file=out)
        print('<navLabel>', file=out)
        print('<text>{} {}</text>'.format(r[0], r[1]), file=out)
        print('</navLabel>', file=out)
        print('<content src="{}"/>'.format("-".join([r[0], r[1]]).lower()+".xhtml"), file=out)
        print('</navPoint>', file=out)
    print('</navMap>', file=out)
    print('</ncx>', file=out)

os.mkdir("epub/META-INF")
with open("epub/META-INF/container.xml", "w") as out:
    print('<?xml version="1.0"?>', file=out)
    print('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">', file=out)
    print('<rootfiles>', file=out)
    print('<rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>', file=out)
    print('</rootfiles>', file=out)
    print('</container>', file=out)

with open("epub/content.opf", "w") as out:
    print('<?xml version="1.0" encoding="utf-8"?>', file=out)
    print('<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">', file=out)
    print('<metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/">', file=out)
    print('<dc:language>en</dc:language>', file=out)
    print('<dc:title>Monica Database</dc:title>', file=out)
    print('<dc:creator opf:file-as="mkbook" opf:role="aut">mkbook</dc:creator>', file=out)
    print('<meta name="cover" content="cover"/>', file=out)
    print('<dc:date>0101-01-01T00:00:00+00:00</dc:date>', file=out)
    print('<dc:contributor opf:role="bkp"></dc:contributor>', file=out)
    print('<dc:identifier id="uuid_id" opf:scheme="uuid">0c159d12-f5fe-4323-8194-f5c652b89f5c</dc:identifier>', file=out)
    print('</metadata>', file=out)
    print('<manifest>', file=out)
    print('<item href="cover.jpeg" id="cover" media-type="image/jpeg"/>', file=out)
    for i, r in enumerate(c.execute("SELECT first_name, last_name FROM contacts WHERE NOT is_partial ORDER BY first_name")):
        print('<item href="{}" id="id{}" media-type="application/xhtml+xml" />'.format("-".join([r[0], r[1]]).lower()+".xhtml", i), file=out)
    print('<item href="page_styles.css" id="page_css" media-type="text/css"/>', file=out)
    print('<item href="stylesheet.css" id="css" media-type="text/css"/>', file=out)
    print('<item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>', file=out)
    print('<item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>', file=out)
    print('</manifest>', file=out)
    print('<spine toc="ncx">', file=out)
    print('<itemref idref="titlepage"/>', file=out)
    for i, r in enumerate(c.execute("SELECT first_name, last_name FROM contacts WHERE NOT is_partial ORDER BY first_name")):
        print('<itemref idref="id{}"/>'.format(i), file=out)
    print('</spine>', file=out)
    print('<guide>', file=out)
    print('<reference href="titlepage.xhtml" type="cover" title="Cover"/>', file=out)
    print('</guide>', file=out)
    print('</package>', file=out)

os.system("cd epub && zip -r monica.epub .")
