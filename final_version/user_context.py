class UserContext:
    def __init__(
            self,
            user_id: int,
            region: str,
            account_type: str,
            beta_program: bool
        ) -> None:
        
        self.user_id = user_id
        self.region = region
        self.account_type = account_type
        self.beta_program = beta_program