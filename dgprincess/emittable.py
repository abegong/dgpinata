from pydantic import BaseModel
from typing import ClassVar, List

annotation_type_lookup = {
    str : "TEXT",
    int : "INTEGER",
    float: "FLOAT",
}

class Emittable(BaseModel):
    """An event that can be recorded in the simulation DB."""

    table_name: ClassVar[str] = None
    column_block_list: ClassVar[List[str]] = [
        "column_block_list",
        "table_name",
    ]

    @classmethod
    def get_create_table_sql(cls) -> str:
        field_str_list = []
        for field_name, field in cls.model_fields.items():
            if field_name in cls.column_block_list:
                continue

            sql_type = annotation_type_lookup[field.annotation]
            field_str_list .append(f"  {field_name} {sql_type}")
        
        field_str = ",\n".join(field_str_list)

        schema_str = f"""
CREATE TABLE {cls.table_name} (
{field_str}
)
"""
        return schema_str
    
    def get_insert_sql(self):
        column_names = [column_name for column_name in self.model_fields.keys() if column_name not in self.column_block_list]
        field_str = ", ".join(column_names)
        value_str = ", ".join(f"'{getattr(self, column_name)}'" for column_name in column_names)

        insert = f"""INSERT INTO {self.table_name} ({field_str}) VALUES ({value_str})"""
        return insert