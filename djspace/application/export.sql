SELECT
    core_genericchoice.name,
    application_undergraduateresearch.project_title, 
    registration_undergraduate.wsgc_school_id,
    auth_user.last_name, auth_user.first_name, auth_user.email,
    core_userprofile.city, core_userprofile.state
FROM
    django_djspace.auth_user
INNER JOIN
    django_djspace.core_userprofile
ON
    auth_user.id = core_userprofile.user_id

INNER JOIN
    django_djspace.core_userprofile_race
ON
    core_userprofile.id = core_userprofile_race.userprofile_id

INNER JOIN
    django_djspace.core_genericchoice
ON
    core_userprofile_race.genericchoice_id = core_genericchoice.id
INNER JOIN
    django_djspace.registration_undergraduate
ON
    auth_user.id = registration_undergraduate.user_id
INNER JOIN
    django_djspace.application_undergraduateresearch
ON
    auth_user.id = application_undergraduateresearch.user_id
ORDER BY
    auth_user.last_name
