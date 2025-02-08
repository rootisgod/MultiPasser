# Uses textual 1.0.0
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, Button, Label, ListView, ListItem
from textual.message import Message
from textual.events import Key


class InputModal(Screen):
    """A modal popup screen that asks the user for text."""
    MODAL = True

    CSS = """
    /* The outer container takes up the full screen and centers its contents. */
    #outer_container {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    /* The actual dialog box. Fixed size, nice border, etc. */
    #dialog_box {
        width: 50;
        height: 10;
        background: $surface;
        border: round $primary;
        padding: 1;
    }
    """

    class Submitted(Message):
        """Message posted when user clicks OK."""
        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    class Cancelled(Message):
        """Message posted when user clicks Cancel or presses Escape."""
        def __init__(self) -> None:
            super().__init__()

    def compose(self) -> ComposeResult:
        """Lay out the modal UI."""
        # A container that fills the screen (outer), then the smaller dialog_box inside it.
        with Container(id="outer_container"):
            with Vertical(id="dialog_box"):
                yield Static("Please type your text:")
                yield Input(id="modal_input", placeholder="Type something...")
                with Horizontal():
                    yield Button("OK", id="ok_button")
                    yield Button("Cancel", id="cancel_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle presses of the OK/Cancel buttons."""
        if event.button.id == "ok_button":
            text_value = self.query_one("#modal_input", Input).value
            self.post_message(self.Submitted(text_value))
            self.dismiss()
        elif event.button.id == "cancel_button":
            self.post_message(self.Cancelled())
            self.dismiss()

    def on_key(self, event: Key) -> None:
        """Close the modal on Escape."""
        if event.key == "escape":
            self.post_message(self.Cancelled())
            self.dismiss()


class MyApp(App):
    """Main application with a title bar, list, and add/delete/quit features."""

    CSS = """
    Screen {
        layout: vertical; /* A simple vertical layout */
    }

    /* Top bar has a fixed height of 1 row, centered text. */
    #top_bar {
        height: 1;
        content-align: center middle;
        background: $accent;
        color: $text;
    }

    /* The list occupies the main space, growing to fill it. */
    #items {
        height: 1fr;      /* Expand to fill leftover space in the vertical layout */
    }

    /* The bottom bar has a fixed height of 1 row. */
    #bottom_bar {
        height: 1;
        content-align: center middle;
        background: $boost;
        color: $text;
    }
    """

    def compose(self) -> ComposeResult:
        """Layout: a title bar, then a ListView, then a bottom bar."""
        # Top bar (header) with the title
        with Container(id="top_bar"):
            yield Static("MultiPasser")

        # Main content: a list of items
        self.list_view = ListView(id="items")
        yield self.list_view

        # Bottom bar (footer) with instructions
        with Container(id="bottom_bar"):
            yield Static("[b]a[/b]: Add  |  [b]d[/b]: Delete  |  [b]q[/b]: Quit")

    def key_a(self) -> None:
        """Pressing 'a' opens the centered input modal."""
        self.push_screen(InputModal())

    def key_d(self) -> None:
        """Pressing 'd' deletes the currently selected item, if any."""
        if self.list_view.index is not None:
            children = list(self.list_view.children)
            if 0 <= self.list_view.index < len(children):
                children[self.list_view.index].remove()

    def key_q(self) -> None:
        """Pressing 'q' quits the app."""
        self.exit()

    def on_input_modal_submitted(self, message: InputModal.Submitted) -> None:
        """Add the user-submitted text to the list."""
        self.list_view.append(ListItem(Label(message.text)))

    def on_input_modal_cancelled(self, message: InputModal.Cancelled) -> None:
        """Modal was canceled or escaped; do nothing except close."""
        pass


if __name__ == "__main__":
    MyApp().run()
