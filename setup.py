from setuptools import setup, find_packages

setup(
    version='1.0.0',
    name='blind-review-parser',
    url='https://github.com/occidere/blind-review-parser',
    description='블라인드의 기업 리뷰를 Elastic Stack 으로 색인 및 시각화 하는 프로젝트',
    packages=find_packages(exclude=['tests', 'docs']),
    package_data={'': ['resources/*.yaml']},
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'pytest',
        'requests',
        'beautifulsoup4',
    ]
)

