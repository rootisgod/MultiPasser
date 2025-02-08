from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button, Label, ListView, ListItem
from textual.message import Message
from textual.events import Key


class InputModal(Screen):
    """A modal popup screen that asks the user for text."""

    MODAL = True  # Tells Textual this screen should be displayed as a modal.

    class Submitted(Message):
        """Message posted when user clicks OK (or otherwise confirms)."""

        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    class Cancelled(Message):
        """Message posted when user clicks Cancel or presses Escape."""

        def __init__(self) -> None:
            super().__init__()

    def compose(self) -> ComposeResult:
        """Lay out the modal UI."""
        with Vertical(id="modal_container"):
            yield Static("Please type your text below:")
            yield Input(id="modal_input", placeholder="Type something...")
            with Horizontal():
                yield Button("OK", id="ok_button")
                yield Button("Cancel", id="cancel_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle presses of the OK/Cancel buttons."""
        if event.button.id == "ok_button":
            text_value = self.query_one("#modal_input", Input).value
            self.post_message(self.Submitted(text_value))
            self.dismiss()  # Close the modal
        elif event.button.id == "cancel_button":
            self.post_message(self.Cancelled())
            self.dismiss()

    def on_key(self, event: Key) -> None:
        """Close the modal on Escape."""
        if event.key == "escape":
            self.post_message(self.Cancelled())
            self.dismiss()


class MyApp(App):
    """Main application with a single list and the ability to open the modal."""

    CSS = """
    #modal_container {
        border: tall $primary;
        padding: 1;
        width: auto;
        height: auto;
        align: center middle;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        """Place a ListView on the screen to show added items."""
        self.list_view = ListView(id="items")
        yield self.list_view

    def key_a(self) -> None:
        """Pressing 'a' opens the input modal."""
        self.push_screen(InputModal())

    def key_d(self) -> None:
        """
        Pressing 'd' will delete the currently selected item from the list,
        if there is one.
        """
        selected_index = self.list_view.index  # None if no selection
        if selected_index is not None:
            children = list(self.list_view.children)
            if 0 <= selected_index < len(children):
                # Remove the child from the DOM by calling its own `remove()`.
                children[selected_index].remove()

                # Optionally, reset or adjust the selection. For instance:
                # self.list_view.index = None

    def on_input_modal_submitted(self, message: InputModal.Submitted) -> None:
        """Add the user-submitted text to the list."""
        self.list_view.append(ListItem(Label(message.text)))

    def on_input_modal_cancelled(self, message: InputModal.Cancelled) -> None:
        """Modal was canceled or escaped; do nothing except close."""
        pass


if __name__ == "__main__":
    MyApp().run()
