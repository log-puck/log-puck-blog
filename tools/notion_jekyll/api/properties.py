"""
Utilities per estrarre valori da proprietà Notion
"""

from typing import Optional, Dict, Any, Union, List


def get_property_value(prop: Optional[Dict[str, Any]]) -> Union[str, List[str], bool, int, float, None]:
    """
    Estrae il valore 'pulito' da un oggetto proprietà Notion.
    
    Gestisce: title, rich_text, select, multi_select, date, relation, checkbox, number
    
    Args:
        prop: Oggetto proprietà Notion (dict con campo "type" e dati specifici)
        
    Returns:
        Valore estratto:
        - str per title, rich_text, select, date
        - List[str] per multi_select, relation (lista di ID)
        - bool per checkbox
        - int/float per number
        - None se prop è None o tipo non supportato
    """
    if not prop:
        return None
        
    prop_type = prop.get("type")
    
    if prop_type == "title":
        title_list = prop.get("title", [])
        if title_list:
            return title_list[0].get("plain_text", "")
        return ""
    elif prop_type == "rich_text":
        rich_text_list = prop.get("rich_text", [])
        if rich_text_list:
            return rich_text_list[0].get("plain_text", "")
        return ""
    elif prop_type == "select":
        select_obj = prop.get("select")
        if select_obj:
            return select_obj.get("name", "")
        return ""
    elif prop_type == "multi_select":
        return [tag.get("name") for tag in prop.get("multi_select", [])]
    elif prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start")
        return None
    elif prop_type is None:
        # Campo esiste ma non ha tipo (campo vuoto o non configurato)
        return None
    elif prop_type == "relation":
        return [rel.get("id") for rel in prop.get("relation", [])]
    elif prop_type == "checkbox":
        return prop.get("checkbox", False)
    elif prop_type == "number":
        return prop.get("number")
    return None
