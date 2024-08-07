from typing import List, Optional
from .common import MetadataError, check_codelist_value, TableMetadata, get_valid_codelist_values

def _generate_metadata_error(catalog: str, schema: str, table: str, field: str, type: str, is_missing: bool, valid_values: Optional[str] = None):
    error_reason = "mangler" if is_missing else "er ugyldig"
    description = f"🔴 Feil: '{field}' {error_reason} i table properties. Type: <{type}>"
    if valid_values != None:
        description += f" - {valid_values}"
    if field == "beskrivelse":
        solution = f"COMMENT ON TABLE {catalog}.{schema}.{table} IS '<<SETT_{field.upper()}_HER>>'"
    else:
        solution = f"ALTER TABLE {catalog}.{schema}.{table} SET TAGS ( '{field}' = '<<SETT_{field.upper()}_HER>>')"
    return MetadataError(catalog=catalog, schema=schema, table=table, column=None, description=description, solution=solution)

def check_beskrivelse(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    if not check_codelist_value(None, metadata.beskrivelse):
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "beskrivelse", "string", metadata.beskrivelse == None))
    
    return context

def check_tilgangsnivaa(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    kodeliste_url = "https://register.geonorge.no/api/register/sikkerhetsniva"

    if not check_codelist_value(kodeliste_url, metadata.tilgangsnivaa):
        valid_values = get_valid_codelist_values(kodeliste_url)
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "tilgangsnivaa", "sikkerhetsnivaa", metadata.tilgangsnivaa == None, f"gyldige verdier: {valid_values}"))
    
    return context

def check_medaljongnivaa(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    valid_values = ["bronse", "sølv", "gull"]
    if not check_codelist_value(None, metadata.medaljongnivaa, valid_values):
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "medaljongnivaa", "valør", metadata.medaljongnivaa == None, f"gyldige verdier: {valid_values}"))
    
    return context

def check_tema(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    kodeliste_url = "https://register.geonorge.no/api/register/inspiretema"

    if not check_codelist_value(kodeliste_url, metadata.tema):
        valid_values = get_valid_codelist_values(kodeliste_url)
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "tema", "inspiretema", metadata.tema == None, f"gyldige verdier: {valid_values}"))
    
    return context

def check_emneord(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    if not check_codelist_value(None, metadata.emneord):
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "emneord", "string", metadata.emneord == None))
    
    return context

def check_bruksomraade(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    kodeliste_url = "https://register.geonorge.no/metadata-kodelister/formal"

    if not check_codelist_value(kodeliste_url, metadata.bruksomraade):
        valid_values = get_valid_codelist_values(kodeliste_url)
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "bruksomraade", "formal", metadata.bruksomraade == None, f"gyldige verdier: {valid_values}"))
    
    return context

def check_begrep(metadata: TableMetadata, context: List[MetadataError]) -> List[MetadataError]:
    kodeliste_url = "https://register.geonorge.no/metadata-kodelister/nasjonal-temainndeling"

    if not check_codelist_value(kodeliste_url, metadata.begrep):
        valid_values = get_valid_codelist_values(kodeliste_url)
        context.append(_generate_metadata_error(metadata.catalog, metadata.schema, metadata.table, "begrep", "nasjonal", metadata.begrep == None, f"gyldige verdier: {valid_values}"))
    
    return context
    
checks_for_valor = {
    "bronse": [check_beskrivelse, check_tilgangsnivaa],
    "sølv":   [check_beskrivelse, check_tema, check_emneord, check_tilgangsnivaa, check_bruksomraade],
    "gull":   [check_beskrivelse, check_tema, check_emneord, check_begrep, check_tilgangsnivaa, check_bruksomraade],
}


def validate_table(metadata: TableMetadata) -> List[MetadataError]:
    validation_context = check_medaljongnivaa(metadata, [])

    if len(validation_context) > 0:
        return validation_context
    
    for check in checks_for_valor[metadata.medaljongnivaa]:
        validation_context = check(metadata, validation_context)

    return validation_context
