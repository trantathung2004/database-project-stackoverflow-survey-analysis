from pydantic import BaseModel
from typing import Optional

class RespondentCreate(BaseModel):
    Age: Optional[str]
    Country: Optional[str]
    EdLevel: Optional[str]
    Employment: Optional[str]
    MainBranch: Optional[str]
    LanguageHaveWorkedWith: Optional[str]
    LanguageWantToWorkWith: Optional[str]
    DatabaseHaveWorkedWith: Optional[str]
    DatabaseWantToWorkWith: Optional[str]
    WebframeHaveWorkedWith: Optional[str]
    WebframeWantToWorkWith: Optional[str]
    LearnCode: Optional[str]
    LearnCodeOnline: Optional[str]
    AISelect: Optional[str]
    AIThreat: Optional[str]
    AIToolCurrently_Using: Optional[str]
    OpSysPersonal_use: Optional[str]
    OpSysProfessional_use: Optional[str]
