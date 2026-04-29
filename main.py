import sys
from random import shuffle
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.binding import Binding


def parse_cards(path: str) -> list[tuple[str, str]]:
    cards = []
    q = a = ""
    for line in open(path):
        line = line.strip()
        if line.startswith("Q>"):
            q = line[2:].strip()
        elif line.startswith("A>"):
            a = line[2:].strip()
            cards.append((q, a))
    return cards


class FCards(App):
    CSS = """
    #card {
        width: 100%;
        height: 100%;
        content-align: center middle;
        text-align: center;
        margin: 0 8;
    }
    #status {
        dock: bottom;
        height: 1;
        text-align: center;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("up,down", "flip", "Flip card"),
        Binding("right", "next", "Next card"),
        Binding("left", "prev", "Previous card"),
    ]

    def __init__(self, cards: list[tuple[str, str]]):
        super().__init__()
        self.cards = cards
        self.index = 0
        self.showing_answer = False

    def compose(self) -> ComposeResult:
        yield Static(id="card")
        yield Static(id="status")

    def on_mount(self) -> None:
        self.update_display()

    def update_display(self) -> None:
        q, a = self.cards[self.index]
        label = "A" if self.showing_answer else "Q"
        text = a if self.showing_answer else q
        self.query_one("#card", Static).update(f"[b]{label}:[/b] {text}")
        self.query_one("#status", Static).update(
            f"Card {self.index + 1}/{len(self.cards)} · ↑↓ flip · ←→ navigate"
        )

    def action_flip(self) -> None:
        self.showing_answer = not self.showing_answer
        self.update_display()

    def action_next(self) -> None:
        if self.index < len(self.cards) - 1:
            self.index += 1
            self.showing_answer = False
            self.update_display()

    def action_prev(self) -> None:
        if self.index > 0:
            self.index -= 1
            self.showing_answer = False
            self.update_display()


def main():
    if len(sys.argv) != 2:
        print("Usage: fcards <path-to-txt>")
        sys.exit(1)
    cards = parse_cards(sys.argv[1])
    shuffle(cards)
    FCards(cards).run()
