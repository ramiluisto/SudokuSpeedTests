from distutils.core import setup, Extension


def main():
  setup(
    name="Fastcount",
    version="1.0.0",
    description="Fastcount module in python",
    author="Mike",
    author_email="mikehuls42@gmail.com",
    ext_modules=[Extension("Fastcount", ["fastcount.c"])]
  )

if (__name__ == "__main__"):
  main()