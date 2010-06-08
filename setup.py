from cream.dist import setup

setup('src/manifest.xml',
    data_files = [
        ('{module_dir}', ['src/service.py', 'src/manifest.xml'])
        ]
    )
