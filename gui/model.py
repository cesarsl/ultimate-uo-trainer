import PySimpleGUI as sg

from gui.config.window import IMAGES, TEXTS

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
    ],
    size=(128, 152),
)

SKILL_STATS_RCOL = sg.Col(
    layout=[
        [sg.T(TEXTS.get("default_skill_name"), key="skill_name", size=(100, 1))],
        [sg.T(TEXTS.get("default_skill_current"), key="skill_current", size=(100, 1))],
        [sg.T(TEXTS.get("default_skill_real"), key="skill_real", size=(100, 1))],
        [sg.T(TEXTS.get("default_skill_cap"), key="skill_cap", size=(100, 1))],
        [sg.T(TEXTS.get("default_skill_session"), key="skill_session", size=(100, 1))],
    ],
    size=(128, 152),
)

SKILL_STATS_FRAME = sg.Frame(
    title="Training Information",
    layout=[
        [
            sg.Image(
                filename=IMAGES.get("default_flag"), size=(304, 32), key="skill_flag"
            )
        ],
        [SKILL_STATS_LCOL, SKILL_STATS_RCOL],
        [sg.T("")],
    ],
    size=(304, 152),
)

SKILL_REQUIREMENTS_MCOL = sg.Col(
    layout=[
        [
            sg.T(
                TEXTS.get("default_requirements"),
                key="requirements_text",
                size=(200, 16),
            )
        ],
    ],
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
