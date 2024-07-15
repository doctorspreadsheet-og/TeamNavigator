import streamlit as st
import os
import csv
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv(".env")

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = OpenAI(api_key=openai_api_key)

# Streamlit interface
# HTML and CSS for the styled title
html_title = """
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-family: 'Arial', sans-serif; font-size: 75px; font-weight: bold; margin: 0; color: rgb(229, 132, 37);">
        Ringler <span style="margin-left: 10px;"> Navigator</span>
    </h1>
</div>
"""

st.markdown("""
    <style>
    .stButton button {
        display: block;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown(html_title, unsafe_allow_html=True)

# Input field for user's message
user_message = st.text_area("", "")

# Dictionary mapping names to image file paths
image_directory = "FACE/"  # Directory where the images are stored
image_map = {
    "James Loseman": "JPLoseman.jpg",
    "CORE BTS": "corebts.png",
    "Joe Loseman": "JLoseman.jpg",
    "Matthew Ross": "MRoss.jpg",
    "Nicol Vargas": "NVargas.jpg",
    "Amy Mailot": "AMailot.jpeg",
    "Andrea Haupert": "AHaupert.jpg",
    "Andrew Peach": "APeach.jpg",
    "Chantelle Gates": "cgates.png",
    "Butch Knowlton": "BKnowlton.png",
    "Dana Crawford": "dcrawford.png",
    "Gerardo Monroy": "GMonroy.jpg",
    "Jordan Kincer": "JKincer.jpg",
    "Julieta Johnson": "JJohnson.png",
    "Karla Dewey": "KDewey.jpg",
    "Katherine Rogerson": "KRogerson.jpg",
    "Kevin Sullivan": "KSullivan.jpeg",
    "Kim Persons": "KPersons.jpg",
    "Kurt Wiewel": "KWiewel.jpg",
    "Leslie Guzowski": "LGuzowski.jpg",
    "Neeru Gupta": "NGupta.jpg",
    "Paula Woodruff": "PWoodruff.jpg",
    "Rebecca Kincer": "RKincer.jpg",
    "Arun Kumar": "AKumar.jpg",
    "Ravi Ellipilla": "REllipilla.jpg",
    "Brian Farrell": "BFarrell.jpg",
    "Peter Jachym": "PJachym.jpg",
    "Lynn DeMauro Clark": "LDeMauroClark.jpg",
    "Peter Early": "PEarly.jpg",
    "Tony Robinson": "TRobinson.jpg",
    "Thomas Rudder": "TRudder.jpg",
    "Ann Marie VonBank": "AMVonBank.jpg",
    "Dawne Ware": "DWare.jpg",
    "William Wright": "WWright.jpg",
    "Jarrod Zea": "Zea.jpg",
    "Simon Rossetter": "SRossetter.jpg",
    "Ryan Olephant": "ROlephant.jpg",
    "Nicole Swift": "NSwift.jpg",
    "Megan Trapletti": "MTrapletti.jpg",
    "Mark Morales": "MMorales.jpg",
    "Erin Eddy": "EEddy.jpg",
    "Duke Wolpert": "DWolpert.jpg",
    "Derek Perkins": "DPerkins.jpg",
    "Dave Nikiel": "DNikiel.jpg",
    "Dennis Alonso": "DAlonso.jpg",
    "Chris Chan": "CChan.jpg",
    "Angus Kennedy": "AKennedy.jpg",
}


# Full list of team data
team_data = [
    {"First Name": "James", "Last Name": "Loseman", "Role": "Senior Systems Administrator", "Email": "JPLoseman@RinglerAssociates.Com", "Phone": "462-252-4275", "Squad": "IT"},
    {"First Name": "Joe", "Last Name": "Loseman", "Role": "COO", "Email": "JLoseman@RinglerAssociates.Com", "Phone": "524-914-3281", "Squad": "Executive"},
    {"First Name": "Matthew", "Last Name": "Ross", "Role": "National Director of Business Development", "Email": "MRoss@RinglerAssociates.Com", "Phone": "567-318-2891", "Squad": "Marketing"},
    {"First Name": "Nicol", "Last Name": "Vargas", "Role": "CFO", "Email": "NVargas@RinglerAssociates.Com", "Phone": "422-467-1645", "Squad": "Finance"},
    {"First Name": "Amy", "Last Name": "Mailot", "Role": "Portfolio Manager", "Email": "AMailot@RinglerAssociates.Com", "Phone": "864-976-4100", "Squad": "IT"},
    {"First Name": "Andrea", "Last Name": "Haupert", "Role": "Brand Manager", "Email": "AHaupert@RinglerAssociates.Com", "Phone": "172-232-4349", "Squad": "Marketing"},
    {"First Name": "Andrew", "Last Name": "Peach", "Role": "Marketing Coach", "Email": "APeach@RinglerAssociates.Com", "Phone": "943-127-3889", "Squad": "Marketing"},
    {"First Name": "Butch", "Last Name": "Knowlton", "Role": "CIO", "Email": "BKnowlton@RinglerAssociates.Com", "Phone": "583-619-2872", "Squad": "Executive"},
    {"First Name": "Dana", "Last Name": "Crawford", "Role": "Azure Dev Ops Administrator", "Email": "DCrawford@RinglerAssociates.Com", "Phone": "330-850-4545", "Squad": "IT"},
    {"First Name": "Gerardo", "Last Name": "Monroy", "Role": "CEO/President", "Email": "GMonroy@RinglerAssociates.Com", "Phone": "852-891-3077", "Squad": "Executive"},
    {"First Name": "Jordan", "Last Name": "Kincer", "Role": "Creatio/DASH Lead Developer", "Email": "JKincer@RinglerAssociates.Com", "Phone": "454-329-8386", "Squad": "IT"},
    {"First Name": "Julieta", "Last Name": "Johnson", "Role": "Executive Assistant to the COO", "Email": "JJohnson@RinglerAssociates.Com", "Phone": "649-631-5713", "Squad": "Operations"},
    {"First Name": "Karla", "Last Name": "Dewey", "Role": "Staff Accountant Accounts Payable", "Email": "KDewey@RinglerAssociates.Com", "Phone": "188-827-9705", "Squad": "Finance"},
    {"First Name": "Katherine", "Last Name": "Rogerson", "Role": "Service Center", "Email": "KRogerson@RinglerAssociates.Com", "Phone": "587-232-3345", "Squad": "Service Center"},
    {"First Name": "Kevin", "Last Name": "Sullivan", "Role": "Director IT, Data & Analytics", "Email": "KSullivan@RinglerAssociates.Com", "Phone": "521-696-5087", "Squad": "IT"},
    {"First Name": "Kim", "Last Name": "Persons", "Role": "Staff Accountant Accounts Receivable", "Email": "KPersons@RinglerAssociates.Com", "Phone": "347-459-2703", "Squad": "Finance"},
    {"First Name": "Kurt", "Last Name": "Wiewel", "Role": "AVP IT Infrastructure", "Email": "KWiewel@RinglerAssociates.Com", "Phone": "133-474-6861", "Squad": "IT"},
    {"First Name": "Leslie", "Last Name": "Guzowski", "Role": "Accounting Manager", "Email": "LGuzowski@RinglerAssociates.Com", "Phone": "872-944-5930", "Squad": "Finance"},
    {"First Name": "Neeru", "Last Name": "Gupta", "Role": "Quality Control", "Email": "NGupta@RinglerAssociates.Com", "Phone": "433-682-9865", "Squad": "IT"},
    {"First Name": "Paula", "Last Name": "Woodruff", "Role": "Corporate Meetings/Events", "Email": "PWoodruff@RinglerAssociates.Com", "Phone": "424-907-9538", "Squad": "Operations"},
    {"First Name": "Rebecca", "Last Name": "Kincer", "Role": "HR Manager", "Email": "RKincer@RinglerAssociates.Com", "Phone": "566-003-4647", "Squad": "HR"},
    {"First Name": "Chantelle", "Last Name": "Gates", "Role": "Client Reporting", "Email": "CGates@RinglerAssociates.Com", "Phone": "716-256-6221", "Squad": "Service Center"},
    {"First Name": "CORE", "Last Name": "BTS", "Role": "Level One Customer Support", "Email": "CBTS@RinglerAssociates.Com", "Phone": "491-456-9990", "Squad": "IT"},
    {"First Name": "Arun", "Last Name": "Kumar", "Role": "Senior Data Engineer", "Email": "AKumar@RinglerAssociates.Com", "Phone": "988-333-3373", "Squad": "IT"},
    {"First Name": "Ravi", "Last Name": "Ellipilla", "Role": "Full Stack Developer", "Email": "REllipilla@RinglerAssociates.Com", "Phone": "571-065-5091", "Squad": "IT"},
    {"First Name": "Brian", "Last Name": "Farrell", "Role": "Chairman of the Board", "Email": "BFarrell@RinglerAssociates.Com", "Phone": "188-827-9705", "Squad": "Ringler Board of Directors"},
    {"First Name": "Peter", "Last Name": "Jachym", "Role": "Vice Chairman of the Board", "Email": "PJachym@RinglerAssociates.Com", "Phone": "587-232-3345", "Squad": "Ringler Board of Directors"},
    {"First Name": "Lynn", "Last Name": "DeMauro Clark", "Role": "Board Member", "Email": "LDeMauroClark@RinglerAssociates.Com", "Phone": "521-696-5087", "Squad": "Ringler Board of Directors"},
    {"First Name": "Peter", "Last Name": "Early", "Role": "Board Member", "Email": "PEarly@RinglerAssociates.Com", "Phone": "347-459-2703", "Squad": "Ringler Board of Directors"},
    {"First Name": "Tony", "Last Name": "Robinson", "Role": "Board Member", "Email": "TRobinson@RinglerAssociates.Com", "Phone": "133-474-6861", "Squad": "Ringler Board of Directors"},
    {"First Name": "Thomas", "Last Name": "Rudder", "Role": "Board Member", "Email": "TRudder@RinglerAssociates.Com", "Phone": "872-944-5930", "Squad": "Ringler Board of Directors"},
    {"First Name": "Ann Marie", "Last Name": "VonBank", "Role": "Board Member", "Email": "AVonBank@RinglerAssociates.Com", "Phone": "433-682-9865", "Squad": "Ringler Board of Directors"},
    {"First Name": "Dawne", "Last Name": "Ware", "Role": "Board Member", "Email": "DWare@RinglerAssociates.Com", "Phone": "424-907-9538", "Squad": "Ringler Board of Directors"},
    {"First Name": "William", "Last Name": "Wright", "Role": "Board Member", "Email": "WWright@RinglerAssociates.Com", "Phone": "566-003-4647", "Squad": "Ringler Board of Directors"},
    {"First Name": "Mike", "Last Name": "Zea", "Role": "Board Member", "Email": "MZea@RinglerAssociates.Com", "Phone": "433-682-9865", "Squad": "Ringler Advisory Board"},
    {"First Name": "Jarrod", "Last Name": "Zea", "Role": "Advisory Board", "Email": "JZea@RinglerAssociates.Com", "Phone": "424-907-9538", "Squad": "Ringler Advisory Board"},
    {"First Name": "Simon", "Last Name": "Rossetter", "Role": "Advisory Board", "Email": "SRossetter@RinglerAssociates.Com", "Phone": "566-003-4647", "Squad": "Ringler Advisory Board"},
    {"First Name": "Ryan", "Last Name": "Olephant", "Role": "Advisory Board", "Email": "ROlephant@RinglerAssociates.Com", "Phone": "433-682-9866", "Squad": "Ringler Advisory Board"},
    {"First Name": "Nicole", "Last Name": "Swift", "Role": "Advisory Board", "Email": "NSwift@RinglerAssociates.Com", "Phone": "424-907-9539", "Squad": "Ringler Advisory Board"},
    {"First Name": "Megan", "Last Name": "Trapletti", "Role": "Advisory Board", "Email": "MTrapletti@RinglerAssociates.Com", "Phone": "566-003-4648", "Squad": "Ringler Advisory Board"},
    {"First Name": "Mark", "Last Name": "Morales", "Role": "Advisory Board", "Email": "MMorales@RinglerAssociates.Com", "Phone": "433-682-9867", "Squad": "Ringler Advisory Board"},
    {"First Name": "Erin", "Last Name": "Eddy", "Role": "Advisory Board", "Email": "EEddy@RinglerAssociates.Com", "Phone": "424-907-9540", "Squad": "Ringler Advisory Board"},
    {"First Name": "Duke", "Last Name": "Wolpert", "Role": "Advisory Board", "Email": "DWolpert@RinglerAssociates.Com", "Phone": "566-003-4649", "Squad": "Ringler Advisory Board"},
    {"First Name": "Derek", "Last Name": "Perkins", "Role": "Advisory Board", "Email": "DPerkins@RinglerAssociates.Com", "Phone": "433-682-9868", "Squad": "Ringler Advisory Board"},
    {"First Name": "Dave", "Last Name": "Nikiel", "Role": "Advisory Board", "Email": "DNikiel@RinglerAssociates.Com", "Phone": "424-907-9541", "Squad": "Ringler Advisory Board"},
    {"First Name": "Dennis", "Last Name": "Alonso", "Role": "Advisory Board", "Email": "DAlonso@RinglerAssociates.Com", "Phone": "566-003-4650", "Squad": "Ringler Advisory Board"},
    {"First Name": "Chris", "Last Name": "Chan", "Role": "Advisory Board", "Email": "CChan@RinglerAssociates.Com", "Phone": "433-682-9869", "Squad": "Ringler Advisory Board"},
    {"First Name": "Angus", "Last Name": "Kennedy", "Role": "Advisory Board", "Email": "AKennedy@RinglerAssociates.Com", "Phone": "424-907-9542", "Squad": "Ringler Advisory Board"}
]



# Function to display team member information along with their image
def display_team_member(name, role, email, phone, squad):
    st.sidebar.markdown(f"**Resource:** {name}")
    st.sidebar.markdown(f"**Role:** {role}")
    st.sidebar.markdown(f"**Email:** {email}")
    st.sidebar.markdown(f"**Phone:** {phone}")
    st.sidebar.markdown(f"**Squad:** {squad}")

    # Display the image if it exists
    image_file = image_map.get(name)
    if image_file:
        image_path = os.path.join(image_directory, image_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.sidebar.image(image, caption=name, width=260)  # Larger image in the sidebar
        else:
            st.sidebar.write("Image file not found for ", name)

# Function to convert team data to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Convert the team data to a pandas DataFrame
df_team = pd.DataFrame(team_data)

# Create a download button for the CSV file in the main content area
csv = convert_df_to_csv(df_team)

# Arrange buttons in the same row using Streamlit columns
col1, col2 = st.columns(2)

with col1:
    if st.button("Search Team"):
        if user_message:
            # Create a chat completion request
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": '''You are the Team Navigator machine, your sole purpose is to identify a resource explicitly from the existing team members. Issues/problems/suggestions will be submitted to you, provide the most appropriate team member to assist based on the team and all their contact information on their own lines without any pretext. 
                    RESPONSE FORMAT (include a line feed/ carriage return for each data point):
                    "Resource\tRavi Ellipilla\nRole\tFull Stack Developer\nEmail\tREllipilla@RinglerAssociates.Com\nPhone\t571-065-5091\nSquad\tIT"

                    TEAM:               
        FIRST NAME	LAST NAME	ROLE	EMAIL	PHONE	Type	SQUAD	Reports To	Area of Responsibility/Expertise
James 	Loseman	Senior Systems Administrator	JPLoseman@RinglerAssociates.Com	462-252-4275	Decision Maker	IT	KWiewel@RinglerAssociates.Com	Systems Strategy, new Ringler IT equipment
Joe	Loseman	COO	JLoseman@RinglerAssociates.Com	524-914-3281	Decision Maker	Executive	GMonroy@RinglerAssociates.Com	Incentive loan, Associate loans, commission split conflicts, ARC (AR Conflict Resolution), EPLI (Employee issue), E&O issue, legal issue, Commission Dispute, conflict with another associate/producer
Matthew 	Ross	National Director of Business Development	MRoss@RinglerAssociates.Com	567-318-2891	Decision Maker	Marketing	NVargas@RinglerAssociates.Com	Docusign, National Accounts, Industry Analytics, Annual Poker Tournament, Annual Golf Event, an issue with a Client, an issue with a Life Company, AIG, Liberty Mutual, Travelers, Chubb, the client portal, a question about a structured settlement product, an attorney fee deferral, a product question, an annuity stream question
Nicol	Vargas	CFO	NVargas@RinglerAssociates.Com	422-467-1645		Finance	GMonroy@RinglerAssociates.Com	Tax Return
Amy	Mailot	Portfolio Manager	AMailot@RinglerAssociates.Com	864-976-4100		IT	BKnowlton@RinglerAssociates.Com	Portfolio management, IT communications
Andrea	Haupert	Brand Manager	AHaupert@RinglerAssociates.Com	172-232-4349		Marketing	NVargas@RinglerAssociates.Com	Marketing Hub, Marketing Management, Event Management, Social Media Management, Website Management, Ringler Store Management, Technical Support for Marketing Tools, attending an industry conference, a marketing campaign, help with the Marketing HUB, Who can help me create an ad, Who can send me the Ringler logo, marketing collateral, Who can help me create a powerpoint, Marketing HUB, Marketing HUB, personalized logo for me, article, email marketing, create an ad, Ringler logo, marketing collateral, help me create a powerpoint, Marketing HUB, Marketing HUB, personalized logo for me, article, email marketing, Ringler’s social media, How can I get started with social media, Who do I send pictures to for social media, Who is in charge of conferences, conference, conference sponsorship, my sponsorships, conferences, Ringler Store, giveaways/promotional items/branded items/shwag
Andrew	Peach	Marketing Coach	APeach@RinglerAssociates.Com	943-127-3889		Marketing	NVargas@RinglerAssociates.Com	Strategic Partners, Business Planning, Associate/Producer Recruiting, Producer Staff Development, Sales Techniques, Goal Setting and Accountability, Succession Planning, Market Expansion, Business Plan Development, Medical Set Assides (MSA), Business Planning for Associates, Producer Recruiting, development of Producer staff, Strategic Partners, Sales Techniques, Sales person, Goal Setting and Accountability, Succession Planning, Market Expansion
Butch	Knowlton	CIO	BKnowlton@RinglerAssociates.Com	583-619-2872	Decision Maker	Executive	GMonroy@RinglerAssociates.Com	Experlogix, Okta, TAI, DASH Manual Quoting
Dana	Crawford	Azure Dev Ops Administrator	DCrawford@RinglerAssociates.Com	330-850-4545	Decision Maker	IT	KWiewel@RinglerAssociates.Com	Pipelines, Repositories, Scrum, Azure
Gerardo	Monroy	CEO/President	GMonroy@RinglerAssociates.Com	852-891-3077	Decision Maker	Executive	GMonroy@RinglerAssociates.Com	Company Vision, Company  Strategy, Company  Initiatives, Company  Objectives, Company Growth Strategy
Jordan	Kincer	Creatio/DASH Lead Developer	JKincer@RinglerAssociates.Com	454-329-8386		IT	KWiewel@RinglerAssociates.Com	DASH Interface, DASH issues
Julieta 	Johnson	Executive Assistant to the COO	JJohnson@RinglerAssociates.Com	649-631-5713		Operations	JLoseman@RinglerAssociates.Com	Payroll File Processing, Old case inquiries, Annuity Inquiries, Case Lookup, Board of Directors Tasks, Insurance Certificates, Stock Options, Financial Reporting, NSSTA Membership, Legal Issues, Customer Service, NSSTA question, an inquiry from an annuitant, obtaining a copy of an insurance certificate, Ringler Stock, monthly financials, business insurance
Karla	Dewey	Staff Accountant Accounts Payable	KDewey@RinglerAssociates.Com	188-827-9705		Finance	NVargas@RinglerAssociates.Com	Autopay requests/updates, ACH requests for distributions or expense reimbursement, Tax payments, Setting up or updating ACH information for direct deposit, Deleting old vendors from Ringler.biz list, Fed Ex checks
Katherine 	Rogerson	Service Center	KRogerson@RinglerAssociates.Com	587-232-3345	Decision Maker	Service Center	GMonroy@RinglerAssociates.Com	Big Kat, SPIN to CRS bridge, Entering and managing premium and split details, Entering and managing files, Adding companies (Carrier, TPA, MSA) to CRS, Adding Liberty adjusters to SPIN, Looking up files in SPIN, CRS Training, RPM Training, Resetting SPIN passwords, Handling Client Reporting, Answering questions on Special Handling and Approved Lists, Handling case referrals from Clients and managing incoming referrals, Providing information on the Service Center, Client Report requests, Editing content in the Ringler Portal, Old Galaher or DSI file lookups, Handling inquiries related to Lawyers and Judges Calculators, Training new Case Managers, Specific referral management (e.g., Sedgwick, Amtrust, American Family, CNA, Optum), Resolving access issues for SPIN
Kevin	Sullivan	Director IT, Data & Analytics	KSullivan@RinglerAssociates.Com	521-696-5087	Decision Maker	IT	BKnowlton@RinglerAssociates.Com	Data Dude, ETL, Python, SQL, Automation, Power BI, SSRS, AI, Data Strategy, Database Administration, Payroll ETL
Kim	Persons	Staff Accountant Accounts Receivable	KPersons@RinglerAssociates.Com	347-459-2703		Finance	NVargas@RinglerAssociates.Com	Commission Inquiries, received commission, Cash flow Report, GL transaction report, Commission Reports, collections, collections reports, CPAs communications
Kurt	Wiewel	AVP IT Infrastructure	KWiewel@RinglerAssociates.Com	133-474-6861	Decision Maker	IT	BKnowlton@RinglerAssociates.Com	IT Vendor Management, Infrastructure Strategy, Infrastructure Monitoring
Leslie	Guzowski	Accounting Manager	LGuzowski@RinglerAssociates.Com	872-944-5930		Finance	NVargas@RinglerAssociates.Com	External split requests, split processing inquiries, Corporation Tax Planning
Neeru	Gupta	Quality Control	NGupta@RinglerAssociates.Com	433-682-9865		IT	BKnowlton@RinglerAssociates.Com	QA, Testing, Regression Testing, Functional Testing, Smoke Testing
Paula	Woodruff	Corporate Meetings/Events	PWoodruff@RinglerAssociates.Com	424-907-9538		Operations	JLoseman@RinglerAssociates.Com	Insurance Licensing, Event Planning, Corporate Meetings & Events, Awards & Gifts, Annuity Applications (PacLife & NYL), Insurance Producer Licensing, Continuing Education, state insurance licenses, insurance continuing education, Ringler company meetings, Ringler Company Trip, signing an annuity application
Rebecca	Kincer	HR Manager	RKincer@RinglerAssociates.Com	566-003-4647	Decision Maker	HR	GMonroy@RinglerAssociates.Com	Empower, Just Works, 401K, Benefits, Onboarding, Bonus Inquiries, Payroll/Shared Payroll (ADP & JustWorks), HR Support, New Hires & Terminations (On-boarding, Off-boarding), Background Screenings, Benefits (Health, 401K/LTD, Workers’ Comp), Producer Efficiency Reports - Payroll/Benefits, NQDC Enrollment/Distributions/Contributions, Fiscal Year-End Profit-Sharing Plan Reporting/Funding, Fiscal Year-End Closeout Salary Reports, General Payroll Communication for Questions/Requests, General HR Communication for Questions/Requests, New Hire, bonus check, obtaining a copy of an worker's comp insurance cert, HR Compliance Issue
Chantelle	Gates	Client Reporting	CGates@RinglerAssociates.Com	716-256-6221		Service Center	KRogerson@RinglerAssociates.Com	Client Reports, Look up old files and provide details: Producer information, Life company information, Claimant assistance, Finding annuities, CRS Case Extract Report, Entering and managing premium and split details, Entering and managing files, Adding companies (Carrier, TPA, MSA) to CRS, Adding Liberty adjusters to CRS, Looking up files in SPIN, Adding companies (Carrier, TPA, MSA) to SPIN, SPIN bridge mapping, Marking cases "Funded" in SPIN, Handling Client Reporting, Answering questions on Special Handling and Approved Lists, Handling case referrals from Clients and managing incoming referrals, Client Report requests, Editing content in the Ringler Portal, Old Galaher or DSI file lookups, Managing premium entries in CRS, Address change updates in the Ringler Office list, Specific referral management (Sedgwick/Amtrust/American Family/CNA/Optum)
CORE	BTS	Level One Customer Support	CBTS@RinglerAssociates.Com	491-456-9990		IT	KWiewel@RinglerAssociates.Com	Desktop Support, Microsoft Products, Email support, log-in support, level one technical support, CRS issues, email issues - Outlook, RPM issues, SPIN issues,Ringlerbiz issue, problem with my PC
Arun	Kumar	Senior Data Engineer	AKumar@RinglerAssociates.Com	988-333-3373		IT	KWiewel@RinglerAssociates.Com	RPM, SPIN, Data Migration, Data Mapping, Data engineering, Resetting SPIN passwords, Resolving access issues for SPIN
Ravi 	Ellipilla	Full Stack Developer	REllipilla@RinglerAssociates.Com	571-065-5091		IT	KWiewel@RinglerAssociates.Com	
Brian	Farrell	Chairman of the Board	BFarrell@RinglerAssociates.Com	188-827-9705	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
Peter	Jachym	Vice Chairman of the Board	PJachym@RinglerAssociates.Com	587-232-3345	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
Lynn	DeMauro Clark	Board Member	LDeMauro Clark@RinglerAssociates.Com	521-696-5087	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
Peter	Early	Board Member	PEarly@RinglerAssociates.Com	347-459-2703	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	FinTech, Wall Street Journal Enthusiast
Tony 	Robinson	Board Member	TRobinson@RinglerAssociates.Com	133-474-6861	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
Thomas 	Rudder	Board Member	TRudder@RinglerAssociates.Com	872-944-5930	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	QBE
Ann Marie	VonBank	Board Member	AVonBank@RinglerAssociates.Com	433-682-9865	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	Ringler newsletter
Dawne	Ware	Board Member	DWare@RinglerAssociates.Com	424-907-9538	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
William	Wright	Board Member	WWright@RinglerAssociates.Com	566-003-4647	Decision Maker	Ringler Board of Directors	BFarrell@RinglerAssociates.Com	
Mike	Zea	Board Member	MZea@RinglerAssociates.Com	433-682-9865		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Jarrod	Zea	Advisory Board	JZea@RinglerAssociates.Com	424-907-9538		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Simon	Rossetter	Advisory Board	SRossetter@RinglerAssociates.Com	566-003-4647		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Ryan	Olephant	Advisory Board	ROlephant@RinglerAssociates.Com	433-682-9866		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Nicole	Swift	Advisory Board	NSwift@RinglerAssociates.Com	424-907-9539		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Megan	Trapletti	Advisory Board	MTrapletti@RinglerAssociates.Com	566-003-4648		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Mark	Morales	Advisory Board	MMorales@RinglerAssociates.Com	433-682-9867		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Erin	Eddy	Advisory Board	EEddy@RinglerAssociates.Com	424-907-9540		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Duke	Wolpert	Advisory Board	DWolpert@RinglerAssociates.Com	566-003-4649		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Derek	Perkins	Advisory Board	DPerkins@RinglerAssociates.Com	433-682-9868		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Dave	Nikiel	Advisory Board	DNikiel@RinglerAssociates.Com	424-907-9541		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Dennis	DAlonso	Advisory Board	DDAlonso@RinglerAssociates.Com	566-003-4650		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Chris	CChan	Advisory Board	CCChan@RinglerAssociates.Com	433-682-9869		Ringler Advisory Board	BFarrell@RinglerAssociates.Com	
Angus	AKennedy	Advisory Board	AAKennedy@RinglerAssociates.Com	424-907-9542		Ringler Advisory Board	BFarrell@RinglerAssociates.Com							
        '''},
                    {"role": "user", "content": user_message}
                ]
            )
            # Extract the response content
            response_content = completion.choices[0].message.content

            # Split the response into lines and parse each line
            resource_list = response_content.strip().split("\n\n")

            for resource_info in resource_list:
                lines = resource_info.strip().split("\n")
                resource_data = {}
                for line in lines:
                    if "\t" in line:
                        key, value = line.split("\t")
                        resource_data[key] = value

                # Display the resource information and image
                display_team_member(
                    resource_data.get("Resource"),
                    resource_data.get("Role"),
                    resource_data.get("Email"),
                    resource_data.get("Phone"),
                    resource_data.get("Squad")
                )
        else:
            st.write("Please enter a message.")

with col2:
    st.download_button(
        label="Export List",
        data=csv,
        file_name='team_data.csv',
        mime='text/csv',
    )
