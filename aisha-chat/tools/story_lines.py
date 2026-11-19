"""Narration + captions for the Aisha chat capabilities film (one entry per voice line).
caption None = no caption (cards already show the words)."""
LINES = [
    # id, text, caption
    ("i1", "Meet Aisha, the money assistant inside Wavvy Wallet.", None),
    ("i2", "Ask her anything, in plain words. Here are six things she can do for you.", None),
    ("h1", "To find her, open Wavvy Wallet, and tap Chat at the bottom.", "Tap *Chat*"),
    ("h2", "The first time, read the short note, then tap, Continue to chat.", "Tap *Continue* *to* *chat*"),
    ("i4", "Let's start with number one.", None),

    ("c1q", "Number one. Ask Aisha about your spending.", None),
    ("c1a", "Type a question, like, how much did I spend this month? Then tap send.", "Type, then tap *send*"),
    ("c1b", "Aisha adds it all up in seconds, and shows how much is still untagged.", "Totals in *seconds*"),
    ("c1c", "Ask where most of your money goes, and she names your biggest costs.", "Your *biggest* *costs*"),

    ("c2q", "Number two. Find any payment, fast.", None),
    ("c2a", "Ask about anyone you pay. Show me my payments to Mary Wanjiku.", "Ask about *anyone*"),
    ("c2b", "She finds every payment, with the dates and fees, and even spots a pattern.", "Dates, fees, *patterns*"),

    ("c3q", "Number three. Tag payments, just by chatting.", None),
    ("c3a", "Tell her what a payment was for. Tag the Kings Court payment as rent.", "Say what it was *for*"),
    ("c3b", "Aisha always asks before she changes anything. Tap, Allow Once.", "She *asks* *first*"),
    ("c3c", "Done. Your rent is tagged, and she offers to do it every month.", "*Tagged!*"),

    ("c4q", "Number four. Cash spending counts too.", None),
    ("c4a", "Paid with cash? Just tell her. I paid two hundred and fifty shillings cash for lunch.", "Just *tell* *her*"),
    ("c4b", "Allow it, and the cash payment is added to your list.", "Cash payment *added*"),

    ("c5q", "Number five. Plan ahead with Aisha.", None),
    ("c5a", "Ask her to plan a weekend trip to Diani, with twenty thousand shillings.", "Plan a *trip*"),
    ("c5b", "She splits it into transport, a place to stay, food, activities, and a little extra, and checks it against your usual spending.", "Split into a *plan*"),
    ("c5c", "Say yes, and she creates a trip category, so you can track every shilling.", "Every shilling *tracked*"),

    ("c6q", "And number six. Aisha can change the app, and listen too.", None),
    ("c6a", "Ask for a purple theme, and the whole app changes colour.", "Ask for a *new* *colour*"),
    ("c6b", "Ask for green again, and it's back.", "Back to *green*"),
    ("c6c", "Rather talk than type? Tap the microphone, and just speak.", "Tap the *mic* and speak"),

    ("o1", "Aisha is in beta, so double check anything important. Open Wavvy Wallet, tap Chat, and say hello.", None),
]
