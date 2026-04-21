from enrich import enrich_company
from scoring import score_account


def main():
    print("\n=== Account Scoring CLI ===\n")

    while True:
        query = input("Enter company name or domain (or type 'exit'): ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print("\n🔍 Enriching company data...")
            account = enrich_company(query)

            print("\n📊 Enriched Account Data:")
            for k, v in account.items():
                print(f"{k}: {v}")

            print("\n🧠 Calculating score...")
            result = score_account(account)

            print("\n✅ Final Result:")
            print(result)

        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()