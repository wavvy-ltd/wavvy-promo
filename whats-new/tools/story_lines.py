"""Narration + captions for the chaptered "What's new" story (one entry per voice line).
caption None = no caption (chapter cards already show the words)."""
LINES = [
    # id, text, caption
    ("i1", "Wavvy Wallet just got better.", None),
    ("i2", "Here are six new updates, explained step by step.", None),
    ("i3", "You'll find them in the What's New popup, after you update.", None),
    ("i4", "Let's start with number one.", None),

    ("c1q", "Do you save or borrow with KCB M-Pesa? Now those messages can go into Wavvy too.", None),
    ("c1a", "If you've allowed SMS access, there's nothing to do. Your KCB M-Pesa messages come in by themselves.", "Comes in *automatically*"),
    ("c1n", "You get a notification, and the payment is already in your list.", "Notified, and *already* *in*"),
    ("c1b", "No SMS access? Tap Add Transaction, choose SMS, paste the message, and tap Next.", "No SMS access? Add *by* *hand*"),
    ("c1c", "Wavvy reads it. Tap Import, and it's saved.", "Tap *Import*"),

    ("c2q", "Number two is for iPhone users with MTN MoMo.", None),
    ("c2a", "You can now bring in your MoMo messages, and even your PDF statements.", "MoMo SMS + *PDF* statements"),
    ("c2b", "Wavvy sorts them into the right categories for you.", "Sorted *for* *you*"),

    ("c3q", "Number three. Tagging simply means saying what a payment was for, like food, rent, or family.", None),
    ("c3a", "Tap any transaction that says, tap to tag.", "Look for *Tap* *to* *tag*"),
    ("c3b", "If your internet drops, the tag screen tells you straight away. Tagging needs internet, so just reconnect, and carry on.", "Offline? It *tells* *you*"),
    ("c3c", "Once you're back online, type what it was for, and pick a tag.", "Type, then pick a *tag*"),
    ("c3d", "Done. The payment is now tagged.", "*Done!*"),

    ("c4q", "Number four. Every time you send money, there's a small fee. Do you know how much they add up to?", None),
    ("c4a", "Open Insights, and find Total Expenses.", "Insights, *Total* *Expenses*"),
    ("c4b", "Swipe that card to the left, and there are your transaction charges for the month.", "Swipe left for *charges*"),

    ("c5q", "Number five. Never forget rent, internet, or Netflix again.", None),
    ("c5a", "Open the menu. Then choose, Bill Reminders.", "Menu, then *Bill* *Reminders*"),
    ("c5b", "Add the bill's name, the due date, and how often it repeats.", "Name, date, *repeat*"),
    ("c5c", "Wavvy reminds you the day before, and on the day.", "Alerts the *day* *before*"),
    ("c5d", "You choose which alerts you get in Settings, under Notifications.", "Settings, *Notifications*"),

    ("c6q", "And number six. Money in and money out are now easier to tell apart, and Rwandan francs are supported.", None),
    ("c6a", "When you tag a payment, money going out shows a minus, and an up arrow.", "*Minus* and up: money *out*"),
    ("c6b", "Money coming in shows a plus, and a down arrow.", "*Plus* and down: money *in*"),
    ("c6c", "And when a new MTN MoMo payment comes in, the notification shows it in Rwandan francs.", "MoMo alerts in *RWF*"),

    ("o1", "That's what's new. Update Wavvy Wallet today, and know where your money is going.", None),
]
