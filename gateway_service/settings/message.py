from pydantic import Field
from pydantic_settings import BaseSettings


class MessageSettings(BaseSettings):
    exchange: str = Field(validation_alias="EXCHANGE", default="gpn_exchange")
    ipr_queue: str = Field(validation_alias="IPR_QUEUE", default="ipr")
    vlp_queue: str = Field(validation_alias="VLP_QUEUE", default="vlp")
    nodal_analysis_queue: str = Field(
        validation_alias="NODAL_ANALYSIS_QUEUE", default="nodal_analysis"
    )
