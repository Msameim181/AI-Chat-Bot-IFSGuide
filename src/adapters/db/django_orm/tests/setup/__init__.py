# import os

# import django
# from django.conf import settings
# from django.test.utils import get_runner


# def setup_database(db_app):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'src.adapters.db.django_orm.db.settings'
#     django.setup()

#     TestRunner = get_runner(settings)
#     _test_runner = TestRunner()

#     _test_runner.setup_test_environment()
#     suite = _test_runner.build_suite([db_app], None)
#     databases = _test_runner.get_databases(suite)
#     # serialized_aliases = set(
#     #     alias for alias, serialize in databases.items() if serialize
#     # )
#     with _test_runner.time_keeper.timed("Total database setup"):
#         _test_runner.interactive = False
#         _test_runner.setup_databases(
#             aliases=databases,
#             serialized_aliases=databases,
#         )

#     return _test_runner


# def teardown_database(test_runner):
#     test_runner.teardown_test_environment()
