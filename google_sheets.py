import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Cognition_Data").sheet1
    return sheet


def save_to_google_sheets(data_dict):
    sheet = connect_sheet()

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data_dict["participant_id"],
        data_dict["name"],
        data_dict["age"],
        data_dict["gender"],
        data_dict["hometown"],
        data_dict["Mother Language"],
        data_dict["qualification"],
        data_dict["service status"],
        data_dict["handedness"],
        data_dict["device used"],
        data_dict["vision status"],
        data_dict["num_attempted"],
        data_dict["num_correct"],
        data_dict["num_w_accuracy"],
        data_dict["num_speed"],
        data_dict["num_ability_score"],
        data_dict["Stroop_error"],
        data_dict["Stroop_mean_RT"],
        data_dict["Stroop_interference"],
        data_dict["MR_acc"],
        data_dict["MR_reaction"],
        data_dict["MR_Timed-out"],
        
    ]

    sheet.append_row(row)