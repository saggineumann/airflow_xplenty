from distutils.core import setup
from airflow_xplenty.version import version

def do_setup():
    setup(
      name = 'airflow_xplenty',
      packages = ['airflow_xplenty', 'airflow_xplenty.operators'],
      version = version,
      description = 'Airflow wrappers for the Xplenty API',
      author = 'Tom Collier',
      author_email = 'collier@apartmentlist.com',
      url = 'https://github.com/apartmentlist/airflow_xplenty',
      download_url =
        ('https://github.com/apartmentlist/airflow_xplenty/archive/' + version + '.tar.gz'),
      keywords = ['airflow', 'xplenty'],
      install_requires = ['airflow (>= 1.7.0)', 'xplenty (>= 1.0.8)'],
      classifiers = []
    )

if __name__ == "__main__":
    do_setup()
