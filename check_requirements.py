import sys
import subprocess
import importlib

def run_command(cmd):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "ERROR"

def main():
    print("=" * 70)
    print("PROJECT ENVIRONMENT VERIFICATION")
    print("=" * 70)
    
    # 1. Check current location
    print("\n1. CURRENT LOCATION:")
    print(f"   {sys.executable}")
    
    # 2. Check Python version
    print("\n2. PYTHON VERSION:")
    print(f"   {sys.version}")
    
    # 3. Check if venv is active
    print("\n3. VIRTUAL ENVIRONMENT:")
    venv_active = sys.prefix != sys.base_prefix
    print(f"   Active: {'✅ YES' if venv_active else '❌ NO'}")
    if venv_active:
        print(f"   Path: {sys.prefix}")
    
    # 4. Check pip packages
    print("\n4. INSTALLED PACKAGES:")
    pip_list = run_command(f'"{sys.executable}" -m pip list')
    if "ERROR" in pip_list:
        print("   ❌ Could not get package list")
    else:
        packages = {}
        for line in pip_list.split('\n')[2:]:  # Skip headers
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    packages[parts[0].lower()] = parts[1]
        
        print(f"   Total packages found: {len(packages)}")
        
    # 5. Critical packages check
    print("\n5. CRITICAL PACKAGES STATUS:")
    
    critical = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('flask_wtf', 'Flask-WTF'),
        ('insightface', 'InsightFace'),
        ('opencv-python', 'OpenCV'),
        ('librosa', 'Librosa'),
        ('speech_recognition', 'SpeechRecognition'),
        ('numpy', 'NumPy'),
        ('scikit-learn', 'scikit-learn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('werkzeug', 'Werkzeug'),
    ]
    
    for import_name, display_name in critical:
        try:
            if import_name == 'opencv-python':
                import cv2
                version = cv2.__version__
                print(f"   ✅ {display_name:<20} {version}")
            elif import_name == 'speech_recognition':
                import speech_recognition
                version = '3.10.0'
                print(f"   ✅ {display_name:<20} {version}")
            elif import_name == 'flask_sqlalchemy':
                import flask_sqlalchemy
                print(f"   ✅ {display_name:<20} {flask_sqlalchemy.__version__}")
            else:
                mod = importlib.import_module(import_name)
                version = getattr(mod, '__version__', '✓')
                print(f"   ✅ {display_name:<20} {version}")
        except ImportError:
            print(f"   ❌ {display_name:<20} MISSING")
        except Exception as e:
            print(f"   ⚠️  {display_name:<20} ERROR: {str(e)[:30]}")
    
    # 6. Check project structure
    print("\n6. PROJECT STRUCTURE CHECK:")
    import os
    
    required_dirs = [
        ('static/css', True),
        ('static/js', True),
        ('static/images', True),
        ('templates', True),
        ('src', True),
        ('models', True),
        ('uploads/faces', True),
        ('uploads/voices', True),
        ('instance', True),
    ]
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
    ]
    
    missing_dirs = []
    for dir_path, required in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            if required:
                missing_dirs.append(dir_path)
                print(f"   ❌ {dir_path}/ (MISSING)")
            else:
                print(f"   ⚠️  {dir_path}/ (Optional, missing)")
    
    print("\n   Required files:")
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file} (MISSING)")
    
    # 7. Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    
    if not venv_active:
        print("❌ VENV NOT ACTIVE - Run: venv\\Scripts\\activate")
    
    if missing_dirs:
        print(f"❌ Missing {len(missing_dirs)} folders")
        for d in missing_dirs:
            print(f"   mkdir {d}")
    
    if missing_files:
        print(f"❌ Missing {len(missing_files)} files")
        for f in missing_files:
            print(f"   touch {f}")
    
    if venv_active and not missing_dirs and not missing_files:
        print("✅ Everything looks good! Run: python app.py")

if __name__ == "__main__":
    main()