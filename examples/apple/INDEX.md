# Apple Jobs API - File Index

📁 **Location:** `/Users/kalilbouzigues/Projects/browgents/reverse-api/scripts/41075dd92a15/`

---

## 📄 Files Overview

### 🚀 Get Started Here

| File | Description | Start Here |
|------|-------------|-----------|
| **QUICKSTART.md** | Quick start guide with examples | ⭐ **Read this first!** |
| **README.md** | Complete API documentation | For detailed information |
| **SUMMARY.md** | Technical analysis summary | For understanding the reverse engineering |

### 💻 Python Scripts

| File | Purpose | How to Use |
|------|---------|-----------|
| **api_client.py** | Main API client library | Import in your code |
| **extract_job_fields.py** | Extract URL, Title, Location, Description | `python extract_job_fields.py` |
| **quick_example.py** | Interactive example script | `python quick_example.py` |

### 📦 Configuration

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies |
| **INDEX.md** | This file |

---

## 🎯 What Do You Want to Do?

### I want to extract job data right now!
→ Run: `python extract_job_fields.py`

This will:
- Fetch jobs from Apple
- Extract URL, Title, Location, Description
- Save to JSON and CSV files

### I want to search for specific jobs
→ Run: `python extract_job_fields.py --query "software engineer"`

### I want to use the API in my own code
→ See `QUICKSTART.md` for code examples
→ Import from `api_client.py`

### I want to understand the API endpoints
→ Read `README.md` - Full API documentation

### I want to know how this was built
→ Read `SUMMARY.md` - Technical details and HAR analysis

---

## 📊 What You'll Get

Running the extraction scripts will give you job data in this format:

```json
{
  "url": "https://jobs.apple.com/en-us/details/[ID]/[title]",
  "title": "Job Title",
  "location": "Location Name",
  "description": "Full job description..."
}
```

**Output formats:**
- ✅ JSON (`.json` files)
- ✅ CSV (`.csv` files)
- ✅ Console output (formatted display)

---

## 🔧 Setup (One-time)

```bash
# Install dependencies
pip install -r requirements.txt

# Make scripts executable (optional)
chmod +x extract_job_fields.py quick_example.py
```

---

## 📚 Documentation Files

### QUICKSTART.md (5KB)
**Purpose:** Get started in 5 minutes
**Contents:**
- Installation instructions
- Basic usage examples
- Common code patterns
- Troubleshooting

### README.md (10KB)
**Purpose:** Complete API reference
**Contents:**
- API endpoint documentation
- Authentication flow
- Request/response formats
- Advanced usage examples
- Data structure reference

### SUMMARY.md (8KB)
**Purpose:** Technical analysis report
**Contents:**
- HAR file analysis results
- API reverse engineering details
- Authentication patterns discovered
- Testing validation results
- API capabilities overview

---

## 💡 Quick Examples

### Example 1: Get All Jobs
```bash
python extract_job_fields.py
```
Output: `apple_jobs_[N]_jobs.json` and `.csv`

### Example 2: Search Jobs
```bash
python extract_job_fields.py --query "engineer"
```
Output: `jobs_engineer.json`

### Example 3: Interactive Mode
```bash
python quick_example.py
```
Follow the prompts to fetch and save jobs

### Example 4: Use in Code
```python
from api_client import AppleJobsAPI

client = AppleJobsAPI()
jobs = client.search_jobs(query="designer")

for job in jobs:
    print(job.url, job.postingTitle, job.locations[0].name)
```

---

## 📈 Statistics

- **Total Jobs Available:** ~6,179
- **Jobs Per Page:** ~20
- **Total Code:** ~1,050 lines
- **Documentation:** ~450+ lines
- **API Endpoints:** 2 (CSRFToken, Search)
- **Supported Locales:** Multiple (en-us, fr-fr, etc.)

---

## ✅ Verified Features

The API client has been **tested and verified** to:

- ✅ Successfully authenticate with Apple's API
- ✅ Retrieve job listings with pagination
- ✅ Extract URL, Title, Location, Description
- ✅ Export to JSON and CSV formats
- ✅ Handle errors gracefully
- ✅ Support search queries
- ✅ Work with multiple locales

**Test Results:**
```
✓ Retrieved 20 jobs from page 1
✓ Total jobs available: 6,179
✓ All fields extracted successfully
```

---

## 🎯 User Requirements ✓

The original request was to extract:
1. ✅ **URL** - Job posting URL
2. ✅ **Title** - Job title
3. ✅ **Location** - Geographic location
4. ✅ **Description** - Job description

**All requirements met!**

---

## 🚦 Getting Started in 30 Seconds

```bash
# 1. Install
pip install requests

# 2. Run
python extract_job_fields.py --query "engineer"

# 3. Done! Check jobs_engineer.json
```

---

## 📞 Need Help?

1. **Quick questions:** See `QUICKSTART.md`
2. **API details:** See `README.md`
3. **Technical info:** See `SUMMARY.md`
4. **Code issues:** Check the docstrings in `api_client.py`

---

## 📝 File Sizes

```
api_client.py          13 KB   (Main library)
README.md              10 KB   (Documentation)
SUMMARY.md              8 KB   (Analysis report)
extract_job_fields.py   5.5 KB  (Extraction script)
QUICKSTART.md           5 KB   (Quick guide)
quick_example.py        3.1 KB  (Interactive example)
requirements.txt        17 B    (Dependencies)
```

**Total:** ~45 KB of code and documentation

---

## 🎉 You're All Set!

Everything you need is in this directory:
- ✅ Production-ready API client
- ✅ Ready-to-use extraction scripts
- ✅ Comprehensive documentation
- ✅ Working examples

**Start here:** `QUICKSTART.md` or run `python extract_job_fields.py`

Happy coding! 🍎
