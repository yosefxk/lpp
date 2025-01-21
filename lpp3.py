import streamlit as st
import requests
import json
import datetime
import pandas as pd

# --- Utility Functions ---

def got_results(request_dictionary):
    return len(request_dictionary["result"]["records"])

def check_handicap(license_plate_number):
    url = f"https://data.gov.il/api/action/datastore_search?resource_id={resource_ids['handicapped']}&filters={{\"{license_plate_field['handicapped']}\":\"{str(license_plate_number)}\"}}"
    try:
        req_dict = requests.get(url, headers={'user-agent': '"datagov-external-client"'}).json()
        return "✅" if req_dict["result"]["total"] == 1 else "❌"
    except requests.exceptions.RequestException as e:
        st.error(f"Error checking handicap status: {e}")
        return "⚠️"  # Indicate an error

# def check_pictures(license_plate_number):
#     url = f"http://iblp.xyz/srch.php?search={str(license_plate_number)}"
#     try:
#         req_text = requests.get(url).text
#         return not ("Nothing found" in req_text)
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error checking for pictures: {e}")
#         return None # Indicate an error

def search_count(license_plate_number):
    if license_plate_number in st.session_state.searches_dict:
        st.session_state.searches_dict[license_plate_number] += 1
    else:
        st.session_state.searches_dict[license_plate_number] = 1
    return f"מספר חיפושים עבור לוחיות זו: {st.session_state.searches_dict[license_plate_number]}"

def add_notification(license_plate_number):
    if license_plate_number not in st.session_state.notifications_monitor:
        st.session_state.notifications_monitor.append(license_plate_number)
        st.toast(f"מספר לוחית חדש התווסף לרשימת המעקב: {license_plate_number}")

# --- Data Dictionaries ---

resource_ids = {
    "private_vehicles" : "053cea08-09bc-40ec-8f7a-156f0677aff3",
    "busses" : "91d298ed-a260-4f93-9d50-d5e3c5b82ce1",
    "motorcycles" : "bf9df4e2-d90d-4c0a-a400-19e15af8e95f",
    "handicapped" : "c8b9f9c8-4612-4068-934f-d4acd2e3c06e",
    "private_import" : "03adc637-b6fe-402b-9937-7c3d3afc9140"
}

hebrew_resource_ids = {
    "private_vehicles" : "כלי רכב פרטיים ומסחריים",
    "busses" :  "אוטובוסים",
    "motorcycles" :  "כלי רכב דו גלגליים",
    "handicapped" :  "כלי רכב עם תג חניה לנכה",
    "private_import" :  "כלי רכב ביבוא אישי"
}

license_plate_field = {
    "busses" : "bus_license_id",
    "motorcycles" : "mispar_rechev",
    "handicapped" : "MISPAR RECHEV",
    "private_vehicles" : "mispar_rechev",
    "private_import" : "mispar_rechev"
}

keys_translation = {
    "private_vehicles" : {
        'mispar_rechev' : "מספר רכב",
        'sug_degem' : "סוג דגם (פרטי/מסחרי)",
        'tozeret_nm' : "שם יצרן",
        'degem_nm' : "שם דגם",
        'ramat_gimur' : "רמת גימור",
        'ramat_eivzur_betihuty' : "רמת אבזור בטיחותי",
        'kvutzat_zihum' : "קבוצת זיהום",
        'shnat_yitzur' : "שנת ייצור",
        'degem_manoa' : "דגם מנוע",
        'mivchan_acharon_dt' : "תאריך מבחן מעשי לרכב (טסט)",
        'tokef_dt' : "תוקף רישיון רכב",
        'baalut' : "סוג בעלות",
        'misgeret' : "מסגרת",
        'tzeva_rechev' : "צבע רכב",
        'zmig_kidmi' : "צמיג קדמי",
        'zmig_ahori' : "צמיג אחורי",
        'sug_delek_nm' : "סוג דלק",
        'moed_aliya_lakvish' : "מועד עליה לכביש",
        'kinuy_mishari' : "כינוי מסחרי",
        'handicapped' : "תו נכה"
    },
    "handicapped" : {
        "MISPAR RECHEV" : "מספר רכב",
        "TAARICH HAFAKAT TAG" : "תאריך הפקת תו נכה",
        "SUG TAV" : "סוג תו נכה"
    },
    "busses" : {
        "operator_nm" : "חברה מפעילה",
        "bus_license_id" : "מספר רכב",
        "stone_proof_nm" : "ממוגן אבנים?",
        "bullet_proof_nm" : "ממוגן ירי?",
        "production_year" : "שנת ייצור",
        "production_country" : "ארץ ייצור",
        "total_kilometer" : "קילוטרז' סה'כ"
    },
    "motorcycles" : {
        "mispar_rechev" : "מספר רכב",
        "tozeret_nm" : "שם תוצר",
        "tozeret_eretz_nm" : "ארץ ייצור",
        "degem_nm" : "שם דגם",
        "shnat_yitzur" : "שנת ייצור",
        "sug_delek_nm" : "סוג דלק",
        "mishkal_kolel" : "משקל כולל",
        "mida_zmig_kidmi" : "צמיג קדמי",
        "mida_zmig_ahori" : "צמיג אחורי",
        "nefach_manoa" : "נפח מנוע",
        "hespek" : "הספק מנוע",
        "misgeret" : "מספר שילדה"
    },
    "private_import" : {
        "mispar_rechev" : "מספר רכב",
        "shilda" : "מספר שילדה",
        "tozeret_cd" : "קוד תוצר",
        "tozeret_nm" : "שם תוצר",
        "sug_rechev_cd" : "קוד סוג רכב",
        "sug_rechev_nm" : "סוג רכב",
        "degem_nm" : "שם דגם",
        "mishkal_kolel" : "משקל כולל",
        "shnat_yitzur" : "שנת יצור",
        "nefach_manoa" : "נפח מנוע",
        "tozeret_eretz_nm" : "ארץ ייצור",
        "degem_manoa" : "דגם מנוע",
        "mivchan_acharon_dt" : "תאריך טסט אחרון",
        "tokef_dt" : "תוקף רישיון רכב",
        "sug_yevu" : "סוג יבוא (חדש/משומש)",
        "moed_aliya_lakvish" : "מועד עליה לכביש",
        "sug_delek_nm" : "סוג דלק"
    }
}

type_of_vehicle = {
    "P" : "פרטי",
    "M" : "מסחרי"
}

# --- Main Search Function ---

def lp_search(lp_to_find):
    all_results = []

    for resource_id in resource_ids:
        if resource_id == "handicapped":
            continue

        url = f"https://data.gov.il/api/action/datastore_search?resource_id={resource_ids[resource_id]}&filters={{\"{license_plate_field[resource_id]}\":\"{str(lp_to_find)}\"}}"
        try:
            req_dict = requests.get(url, headers={'user-agent': '"datagov-external-client"'}).json()

            if req_dict["result"]["total"] == 1:
                result_data = {"מקור מידע": hebrew_resource_ids[resource_id]}
                record = req_dict["result"]["records"][0]

                if resource_id == "private_vehicles":
                    record["sug_degem"] = type_of_vehicle.get(record["sug_degem"], record["sug_degem"]) # Use get with default
                    if record.get("mivchan_acharon_dt"):
                        record["mivchan_acharon_dt"] = f"{record['mivchan_acharon_dt'][8:10]}/{record['mivchan_acharon_dt'][5:7]}/{record['mivchan_acharon_dt'][0:4]}"
                    if record.get("tokef_dt"):
                        record["tokef_dt"] = f"{record['tokef_dt'][8:10]}/{record['tokef_dt'][5:7]}/{record['tokef_dt'][0:4]}"
                    record["handicapped"] = check_handicap(lp_to_find)

                for key, value in record.items():
                    if key in keys_translation[resource_id]:
                        result_data[keys_translation[resource_id][key]] = str(value)
                all_results.append(result_data)

        except requests.exceptions.RequestException as e:
            st.error(f"Error querying {hebrew_resource_ids[resource_id]}: {e}")

    st.markdown(f"<div style='text-align: right;'>{search_count(lp_to_find)}</div>", unsafe_allow_html=True)
    if not all_results:
        add_notification(lp_to_find)
    return all_results

# --- Streamlit App ---

st.markdown("<h1 style='text-align: right;'>חיפוש מספרי רישוי ישראליים</h1>", unsafe_allow_html=True)

# Initialize session state for searches and notifications if they don't exist
if 'searches_dict' not in st.session_state:
    st.session_state.searches_dict = {}
if 'notifications_monitor' not in st.session_state:
    st.session_state.notifications_monitor = []

def perform_search():
    if st.session_state.license_plate_input:
        with st.spinner(f"...מחפש מידע עבור {st.session_state.license_plate_input}"):
            st.session_state.search_results = lp_search(st.session_state.license_plate_input)

st.markdown("<h3 style='text-align: right;'>:הזינו מספר לוחית רישוי לחיפוש</h3>", unsafe_allow_html=True)
license_plate = st.text_input("", key="license_plate_input", on_change=perform_search)

# Initialize search_results in session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if st.session_state.search_results:
    st.markdown("<h2 style='text-align: right;'>תוצאות חיפוש</h2>", unsafe_allow_html=True)
    for result in st.session_state.search_results:
        col1, col2 = st.columns(2)
        for i, (key, value) in enumerate(result.items()):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"<div style='text-align: right; direction: rtl;'><strong>{key}:</strong> {value}</div>", unsafe_allow_html=True)

        license_plate_number = result.get('מספר רכב')
        # if license_plate_number:
        #     has_pictures = check_pictures(license_plate_number)
        #     if has_pictures is True:
        #         st.success(f"<div style='text-align: right; direction: rtl;'>📷 נמצאו תמונות עבור לוחית זו באתר iblp.xyz</div>")
        #     elif has_pictures is False:
        #         st.warning(f"<div style='text-align: right; direction: rtl;'>לא נמצאו תמונות עבור לוחית זו באתר iblp.xyz</div>", unsafe_allow_html=True)
        #     elif has_pictures is None:
        #         st.error(f"<div style='text-align: right; direction: rtl;'>שגיאה בבדיקת תמונות.</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

else:
    if st.session_state.license_plate_input:  # Only show if something was entered
        st.warning("<div style='text-align: right; direction: rtl;'>לא נמצאו תוצאות עבור לוחית זו.</div>", unsafe_allow_html=True)

if st.session_state.notifications_monitor:
    st.sidebar.subheader("לוחיות רישוי במעקב:")
    st.sidebar.write(st.session_state.notifications_monitor)