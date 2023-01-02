from one_piece_scan_bot.one_piece_bot import ContentChecker


def main():
    print(f"Checking new content...")
    content_checker = ContentChecker()
    content_checker.check_releases()
    content_checker.check_artur()
    print(f"Checked new content.")


if __name__ == '__main__':
    main()
