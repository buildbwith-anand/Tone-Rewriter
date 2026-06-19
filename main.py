from tone_rewriter.config import MODEL, TONES
from tone_rewriter.voice import listen
from tone_rewriter.rewriter import rewrite


def main():
    print("=" * 52)
    print(f"   Local Tone Rewriter (with voice)  -  {MODEL}")
    print("=" * 52)

    while True:
        entry = input("\nType your text, or type 'v' to speak it (or 'q' to quit):\n> ")
        command = entry.strip().lower()

        if command in ("q", "quit", "exit"):
            print("\nGoodbye!")
            break

        if command == "v":
            text = listen()
            if not text:
                continue
        elif not entry.strip():
            print("(Nothing entered - try again.)")
            continue
        else:
            text = entry

        print("\nChoose a tone:")
        for key, (name, _description) in TONES.items():
            print(f"  {key}. {name}")
        choice = input("> ").strip()
        if choice not in TONES:
            print("(Not a valid option - using 'Professional'.)")
            choice = "1"
        tone_name, tone_description = TONES[choice]

        print(f"\nRewriting in a {tone_name} tone...\n")
        result = rewrite(text, tone_description)
        print("-" * 52)
        print(result)
        print("-" * 52)


if __name__ == "__main__":
    main()
