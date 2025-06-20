import os
import shutil
import subprocess
import sys

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext

base_path = os.path.abspath(os.path.dirname(__file__))


class NodeJsExtension(Extension):
    def __init__(self, name, source_dir=''):
        super().__init__(name, sources=[])
        self.source_dir = os.path.abspath(source_dir)


class SetupHelper:
    def __init__(
        self,
        source_dir: str,
        ext_dir: str,
        tmp_dir: str,
    ):
        folder_package = ''
        for item in sys.path:
            if 'dist-packages' in item or 'site-packages' in item:
                folder_package = item
                break
        self._source_dir = source_dir
        self._ext_dir = ext_dir
        self._tmp_dir = tmp_dir
        self._folder_package = folder_package

    def clean_old_installation(self):
        # CHECK IF IS INSTALLATION FROM PYPI
        if os.path.isdir(os.path.join(self._source_dir, 'src')):
            try:
                shutil.rmtree(
                    os.path.join(
                        self._folder_package,
                        'herokulls', 'node_modules',
                    ),
                )
            except OSError:
                pass
            try:
                shutil.rmtree(
                    os.path.join(
                        self._folder_package, 'herokulls', 'dist',
                    ),
                ),
            except OSError:
                pass
            try:
                shutil.rmtree(os.path.join(self._tmp_dir))
            except OSError:
                pass

    def run_installation(self):
        # CHECK IF IS INSTALLATION FROM PYPI
        if os.path.isdir(os.path.join(self._source_dir, 'src')):
            # COPY NEEDED FILES
            shutil.copytree(
                os.path.join(self._source_dir, 'src'),
                os.path.join(self._tmp_dir, 'src'),
            )
            shutil.copyfile(
                os.path.join(self._source_dir, 'package.json'),
                os.path.join(self._tmp_dir, 'package.json'),
            )
            shutil.copyfile(
                os.path.join(self._source_dir, 'tsconfig.json'),
                os.path.join(self._tmp_dir, 'tsconfig.json'),
            )
            shutil.copyfile(
                os.path.join(self._source_dir, '.npmignore'),
                os.path.join(self._tmp_dir, '.npmignore'),
            )
            # START COMPILATION
            subprocess.check_call(
                'npm install .',
                shell=True,
                cwd=self._tmp_dir,
            )
            shutil.copytree(
                os.path.join(self._tmp_dir, 'node_modules'),
                os.path.join(self._ext_dir, 'herokulls', 'node_modules'),
            )
            shutil.copytree(
                os.path.join(self._tmp_dir, 'dist'),
                os.path.join(self._ext_dir, 'herokulls', 'dist'),
            )


class NodeJsBuilder(build_ext):
    def run(self):
        super().run()

    def build_extension(self, ext):
        ext_dir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)),
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        sh = SetupHelper(
            ext.source_dir,
            ext_dir,
            self.build_temp,
        )
        sh.clean_old_installation()
        sh.run_installation()


with open(os.path.join(base_path, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='herokulls',
    version='0.1.12',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/pussykillerherokulls',
    author='Frost_Shard',
    license='LGPL-3.0',
    license_file='LICENSE',
    classifiers=[
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    ext_modules=[NodeJsExtension('herokulls')],
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'psutil',
        'screeninfo',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    universal=True,
    cmdclass={
        'build_ext': NodeJsBuilder,
    },
    zip_safe=False,
)
