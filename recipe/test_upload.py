"""Check the installed client's legacy upload label routing without uploading."""

from unittest.mock import patch

from binstar_client.commands import upload
from binstar_client.scripts.cli import main

with (
    patch.object(upload, "_dotorg_upload") as org_upload,
    patch(
        "binstar_client.commands._repo_channels.upload_command",
        side_effect=AssertionError("Unexpected repository upload"),
    ),
):
    main(
        [
            "upload",
            "--user=cf-staging",
            "--channel=main",
            "--private",
            "--force-metadata-update",
            "package.tar.bz2",
        ],
        allow_plugin_main=False,
        exit_=False,
    )

org_upload.assert_called_once()
arguments = org_upload.call_args.args[0]
assert arguments.user == "cf-staging"
assert arguments.labels == ["main"]
assert arguments.channels == []
assert arguments.private
assert arguments.force_metadata_update
