"""Narration + captions for the Aisha reminders film (one entry per voice line).
caption None = no caption (cards already show the words)."""
LINES = [
    # id, text, caption
    ("i1", "Aisha can now set your reminders for you.", None),
    ("i2", "Here are four ways she helps you stay on top of your money.", None),
    ("i4", "Let's start with number one.", None),

    ("c1q", "A weekly reminder to tag your payments.", None),
    ("c1a", "Untagged payments pile up. On your home screen, a new card offers a tagging reminder.", "A new *home* card"),
    ("c1b", "Or just ask Aisha. Remind me to tag my transactions every Friday at six p.m.", "Just *ask* *Aisha*"),
    ("c1c", "Done. Every Friday at six, Wavvy reminds you to tag.", "Fridays at *6* *PM*"),

    ("c2q", "Number two. Never miss a bill.", None),
    ("c2a", "Tell Aisha about the bill. Remind me to pay rent of eighteen thousand shillings on the fifth of every month.", "Tell her the *bill*"),
    ("c2b", "She doesn't guess. She asks when you'd like to be alerted.", "She *asks* *first*"),

    ("c3q", "Number three. You choose the alerts.", None),
    ("c3a", "Answer, two days before, and one day before.", "Pick your *alerts*"),
    ("c3b", "Your rent reminder is saved, with an alert on the due date too.", "Rent reminder *saved*"),

    ("c4q", "And number four. Check and tidy your reminders.", None),
    ("c4a", "Ask, what bill reminders do I have? Aisha lists them all.", "See them *all*"),
    ("c4b", "She even spots a duplicate rent reminder, and deletes it when you say yes.", "Duplicates *removed*"),
    ("c4c", "Change a time just by asking. Move my Netflix reminder to eight p.m.", "Change it by *asking*"),
    ("c4d", "Everything shows up in Bill Reminders. Your tagging reminder is in Settings, under Notifications.", "All in *one* *place*"),

    ("o1", "Open Wavvy Wallet, tap Chat, and let Aisha remind you.", None),
]
