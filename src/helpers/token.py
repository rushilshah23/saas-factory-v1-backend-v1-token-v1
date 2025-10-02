from dataclasses import dataclass

@dataclass
class Token:
    access_token:str = None
    refresh_token:str = None

    def to_dict(self):
        return {
            'access_token':self.access_token,
            # 'refresh_token':self.refresh_token
        }