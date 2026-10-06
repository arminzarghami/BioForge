# BioForge core contract

این بسته کد بخش ۱ است. چهار بخش دیگر باید دقیقاً توابع زیر را در اختیار
`bioforge.pipeline` قرار دهند:

```python
# bioforge/fasta.py — مبینا
def parse_fasta(path: Path) -> list[FastaRecord]: ...

# bioforge/data.py — احسان
def load_data(data_dir: Path) -> tuple[dict[str, str], dict[str, float]]: ...

# bioforge/orf.py — محمد
def find_orfs(dna_sequence: str) -> list[ORFCandidate]: ...

# bioforge/processing.py — رضا
def process_orfs(
    candidates: list[ORFCandidate],
    codon_table: dict[str, str],
    amino_weights: dict[str, float],
    filters: FilterOptions,
) -> list[ORFResult]: ...
```

مدل‌های مشترک داخل `bioforge/models.py` هستند. اعضای تیم نباید نسخهٔ جداگانه‌ای
از این مدل‌ها بسازند و باید همان‌ها را import کنند.

## رفتار مورد انتظار بخش‌ها

- `parse_fasta` ترتیب رکوردها را حفظ می‌کند. متن قبل از اولین Header و رکورد دارای
  Header بدون ID یا Sequence را با `FastaFormatError` در logger پروژه ثبت می‌کند،
  همان بخش را کنار می‌گذارد و خواندن فایل را ادامه می‌دهد. اگر فایل خالی باشد یا
  در پایان هیچ رکورد قابل پردازشی نمانده باشد، `FastaFormatError` به pipeline
  برمی‌گرداند تا اجرای کلی متوقف شود.
- `load_data` برای خط خراب یا دادهٔ ناقص `DataFileError` می‌دهد و شمارهٔ خط را
  در پیام قرار می‌دهد. جدول کدون باید ۶۴ عضو داشته باشد و تمام آمینواسیدهای غیر
  از `*` باید در جدول وزن موجود باشند.
- `find_orfs` ترتیب Forward، Reverse، frameهای ۰ تا ۲ و سپس startهای صعودی را
  حفظ می‌کند. `start_pos` صفرمبنا و نسبت به DNA اصلی است. برای Reverse از فرمول
  `DNA length - 1 - reverse start` استفاده می‌شود و هر `AUG` یک شروع مستقل است.
- `process_orfs` ترجمه، وزن، یافتن Motif و هر سه فیلتر را اجرا می‌کند. مرزهای وزن
  شامل هستند، تمام شرط‌های فعال باید برقرار باشند و وزن از جمع وزن residueها
  به‌اضافهٔ `18.015` به دست می‌آید.

## اجرای تست‌های core

از ریشهٔ این پوشه:

```bash
python -m unittest discover -s tests -v
```

## اجرای نهایی پس از Merge شدن بقیهٔ بخش‌ها

```bash
python main.py \
  --input input/input.fasta \
  --out output/ \
  --min-length 4
```

نمونه با فیلترهای اختیاری:

```bash
python main.py \
  --input input/input.fasta \
  --out output/ \
  --min-length 4 \
  --min-weight 200 \
  --max-weight 2000 \
  --motif MKT
```

## سه تصمیم مناسب برای توضیح Pull Request

1. مدل‌های مشترک در `models.py` متمرکز شدند تا قرارداد بین شاخه‌های موازی یکسان
   بماند.
2. خطاهای `FastaFormatError` و `InvalidSequenceError` داخل حلقهٔ رکوردها مدیریت
   می‌شوند، اما خطای فایل داده به سطح اصلی می‌رسد و اجرا را متوقف می‌کند.
3. شناسه‌های `BFG_###` بعد از اجرای همهٔ فیلترها ساخته می‌شوند تا شماره‌ها پیوسته
   و وابسته به خروجی نهایی باشند.
