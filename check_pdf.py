from pathlib import Path
import os


def check_pdf_naive(filename: str) -> bool:
    with open(filename, 'rb') as f:
        if f.read(5) == b'%PDF-':
            return True
        return False


if __name__ == '__main__':
    path = Path('data')
    os.makedirs('corrupted-data', exist_ok=True)

    for pdf in path.glob('*.pdf'):
        if not check_pdf_naive(pdf):
            print(f'Corrupted pdf {pdf}')
            pdf.rename(f'corrupted-data/{pdf.name}')
