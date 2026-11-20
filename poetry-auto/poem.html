name: Publish Chinese poem every two days

on:
  schedule:
    # Daily check: script uses America/New_York date and the Nov 19 anchor.
    - cron: '13 14 * * *'
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Test only (default true, does not publish)'
        type: boolean
        default: true

permissions:
  contents: write

concurrency:
  group: poetry-serial-publication
  cancel-in-progress: false

jobs:
  publish:
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: true
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install publisher dependency
        run: pip install 'openai>=1.70,<4'
      - name: Verify audio tool
        run: ffmpeg -version | head -n 1
      - name: Publish next numbered poem when due
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          POETRY_VISION_MODEL: gpt-4.1
          POETRY_TTS_MODEL: gpt-4o-mini-tts
        run: |
          if [[ "${{ github.event_name }}" == "workflow_dispatch" && "${{ inputs.dry_run }}" == "true" ]]; then
            python poetry_autopublish.py --dry-run
          else
            python poetry_autopublish.py
          fi
      - name: Commit publication (if changed)
        if: ${{ github.event_name == 'schedule' || inputs.dry_run == false }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add index.html poetry.html poetry-auto/
          if ! git diff --cached --quiet; then
            git commit -m "诗词里的中国：自动发布下一首"
            git push
          fi
