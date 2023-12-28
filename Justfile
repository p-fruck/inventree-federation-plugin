compose := "docker-compose -f docker-compose.yml -f '" + justfile_directory() + "/docker-compose.override.yml'"

@up *flags:
	cd ../InvenTree && INVENTREE_FEDERATION_PATH={{ justfile_directory() }} {{ compose }} up {{ flags }}
	cd ../InvenTree2 && INVENTREE_FEDERATION_PATH={{ justfile_directory() }} {{ compose }} up {{ flags }}

@down *flags:
	cd ../InvenTree && {{ compose }} down {{ flags }}
	cd ../InvenTree2 && {{ compose }} down {{ flags }}
