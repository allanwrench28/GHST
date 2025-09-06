from nicegui import ui

ui.colors(dark=True)
ui.label('If you see a dark background, NiceGUI dark mode works!').style('font-size:2em; color:#fff; background:#222; padding:2em; border-radius:16px; margin:2em;')
ui.run(title='NiceGUI Dark Mode Test')
