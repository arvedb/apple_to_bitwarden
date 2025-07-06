import csv
import json
import uuid
import click

@click.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument("output_file", type=click.Path(dir_okay=False, writable=True, allow_dash=True))
@click.option("--folder", "-f", "folder_name", help="Name of the Bitwarden folder to put entries into.")
def cli(input_file, output_file, folder_name):
    """Converts Apple password CSV exports to Bitwarden JSON format."""
    
    folder_id = None
    folders = []
    if folder_name:
        folder_id = str(uuid.uuid4())
        folders.append({
            "id": folder_id,
            "name": folder_name
        })

    grouped_logins = {}
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row.get("Username")
                password = row.get("Password")

                if not username and not password:
                    continue

                key = (username, password)
                if key not in grouped_logins:
                    grouped_logins[key] = {
                        "name": row.get("Title"),
                        "username": username,
                        "password": password,
                        "notes": set(),
                        "uris": set(),
                        "totp": None
                    }
                
                if row.get("URL"):
                    grouped_logins[key]["uris"].add(row.get("URL"))
                if row.get("Notes"):
                    grouped_logins[key]["notes"].add(row.get("Notes"))
                
                if not grouped_logins[key]["totp"] and row.get("OTPAuth"):
                    grouped_logins[key]["totp"] = row.get("OTPAuth")

    except Exception as e:
        click.echo(f"Error reading or processing CSV file: {e}", err=True)
        raise click.Abort()

    items = []
    for login_data in grouped_logins.values():
        item = {
            "id": str(uuid.uuid4()),
            "organizationId": None,
            "folderId": folder_id,
            "type": 1,
            "reprompt": 0,
            "name": login_data["name"],
            "notes": "\n".join(sorted(list(login_data["notes"]))),
            "favorite": False,
            "login": {
                "uris": [{"match": None, "uri": uri} for uri in sorted(list(login_data["uris"]))],
                "username": login_data["username"],
                "password": login_data["password"],
                "totp": login_data["totp"],
            },
            "collectionIds": [],
            "fields": []
        }
        items.append(item)

    bitwarden_export = {
        "encrypted": False,
        "folders": folders,
        "items": items
    }

    try:
        with click.open_file(output_file, mode='w', encoding='utf-8') as jsonfile:
            json.dump(bitwarden_export, jsonfile, indent=2)
    except Exception as e:
        click.echo(f"Error writing JSON file: {e}", err=True)
        raise click.Abort()

    click.echo(f"Successfully converted {len(items)} login items.", err=True)
    click.echo(f"Output written to {output_file}", err=True)

if __name__ == '__main__':
    cli()
