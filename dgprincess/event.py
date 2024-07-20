from pydantic import BaseModel, Field
from typing import ClassVar, List, Tuple
from uuid import uuid4

annotation_type_lookup = {
    str : "TEXT",
    int : "INTEGER",
}

class Event(BaseModel):
    """An event that can be recorded in the simulation DB."""

    table_name: ClassVar[str]

    @classmethod
    @property
    def schema_sql(cls) -> str:
        field_str_list = []
        for field_name, field in cls.model_fields.items():
            sql_type = annotation_type_lookup[field.annotation]
            field_str_list .append(f"  {field_name} {sql_type}")
        
        field_str = ",\n".join(field_str_list)

        schema_str = f"""
CREATE TABLE {cls.table_name} (
{field_str}
)
"""
        
        print(schema_str)
        return schema_str
    
    @property
    def insert_sql(self):
        field_str = ", ".join(self.model_fields.keys())
        value_str = ", ".join(f"'{getattr(self, field)}'" for field in self.model_fields.keys())

        insert = f"""INSERT INTO {self.table_name} ({field_str}) VALUES ({value_str})"""

        # print(insert)
        return insert