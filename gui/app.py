import PySimpleGUI as sg

# Constants

MAIN_TITLE = "Ultimate UO Trainer v1.0"
MAIN_SIZE = (640, 480)
DEFAULT_REQ = "Select a skill before proceding."
ASSETS_DEFAULT_FLAG = "../assets/img/flag_blank.png"

# Global configuration

sg.ChangeLookAndFeel("SystemDefault")

# Layout Definition

SKILL_STATS_LCOL = sg.Col(
    layout=[
        [sg.T("Skill", auto_size_text=True)],
        [sg.T("Current", auto_size_text=True)],
        [sg.T("Real", auto_size_text=True)],
        [sg.T("Cap", auto_size_text=True)],
        [sg.T("Session Gain", auto_size_text=True)],
        [sg.T("Total Gain", auto_size_text=True)],
    ],
    size=(128, 152),
)

SKILL_STATS_RCOL = sg.Col(
    layout=[
        [sg.T("", key="skill_name", size=(100, 1))],
        [sg.T("", key="skill_current", size=(100, 1))],
        [sg.T("", key="skill_real", size=(100, 1))],
        [sg.T("", key="skill_cap", size=(100, 1))],
        [sg.T("", key="skill_session", size=(100, 1))],
        [sg.T("", key="skill_total", size=(100, 1))],
    ],
    size=(128, 152),
)

SKILL_STATS_FRAME = sg.Frame(
    title="Training Information",
    layout=[
        [sg.Image(filename=ASSETS_DEFAULT_FLAG, size=(304, 32), key="skill_flag")],
        [SKILL_STATS_LCOL, SKILL_STATS_RCOL],
        [sg.T("")],
    ],
    size=(304, 152),
)

SKILL_REQUIREMENTS_MCOL = sg.Col(
    layout=[[sg.T(DEFAULT_REQ, key="requirements_text", size=(200, 16),)],],
    size=(272, 152),
)

SKILL_REQUIREMENTS_FRAME = sg.Frame(
    title="Instructions",
    layout=[[sg.T("", size=(1, 2))], [SKILL_REQUIREMENTS_MCOL], [sg.T("")]],
    size=(304, 152),
)

SKILL_SELECTOR = sg.Combo(
    values=["Choose a skill..."],
    default_value="Choose a skill...",
    enable_events=True,
    size=(604, 16),
    key="skill_combo",
)

MAIN_LAYOUT = [
    [sg.Text("")],
    [SKILL_SELECTOR],
    [sg.Text("")],
    [SKILL_REQUIREMENTS_FRAME, sg.VerticalSeparator(), SKILL_STATS_FRAME],
    [sg.T("")],
    [
        sg.Button("Start", size=(38, 1), key="start"),
        sg.Button("Stop", size=(40, 1), key="stop", disabled=True),
    ],
    [sg.T("")],
    [sg.StatusBar("", size=(640, 1), key="status_bar")],
]
