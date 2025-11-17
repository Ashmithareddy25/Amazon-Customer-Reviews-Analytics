import os
import shutil

# Path where you downloaded Hadoop binaries
SOURCE = r"C:\Users\saiha\Desktop\hadoop\hadoop-3.2.2\bin"

# Path where Spark expects Hadoop on Windows
TARGET = r"C:\hadoop\bin"

print("🚀 Starting Hadoop setup...")

# Create required directories
if not os.path.exists(r"C:\hadoop"):
    os.makedirs(r"C:\hadoop")
    print("📁 Created folder: C:\\hadoop")

if not os.path.exists(TARGET):
    os.makedirs(TARGET)
    print("📁 Created folder: C:\\hadoop\\bin")

# Copy files
print("\n📥 Copying Hadoop winutils files...")
files = os.listdir(SOURCE)

success = 0
for file in files:
    src_file = os.path.join(SOURCE, file)
    dst_file = os.path.join(TARGET, file)
    shutil.copy2(src_file, dst_file)
    success += 1

print(f"✔ Copied {success} files to C:\\hadoop\\bin")

# Verify
if os.path.exists(os.path.join(TARGET, "winutils.exe")):
    print("\n🎉 Hadoop winutils setup successfully completed!")
    print("👉 Now set environment variables:")
    print("   HADOOP_HOME = C:\\hadoop")
    print("   Add to PATH: C:\\hadoop\\bin")
else:
    print("❌ winutils.exe NOT FOUND. Something went wrong!")
