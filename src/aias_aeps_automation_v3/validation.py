"""Public module supporting AEPS repeatable generation and delivery automation."""
class ValidationEngine:
    """Execute the public ValidationEngine operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    def validate_ir(self,ir):
        """Validate ir for AEPS repeatable generation and delivery automation and report explicit issues."""
        issues=[]
        if not ir.get('contracts'): issues.append('missing_contracts')
        if not ir.get('architecture_refs'): issues.append('missing_architecture_reference')
        if not ir.get('adr_refs'): issues.append('missing_adr_reference')
        for c in ir.get('contracts',[]):
            if not c.get('acceptance_criteria'): issues.append(c.get('requirement_id','unknown')+':missing_acceptance_criteria')
        return issues
    def validate_workspace(self,ws):
        """Report missing source, test and documentation directories in a generated workspace."""
        return [f'missing_{n}' for n in ('src','tests','docs') if not (ws/n).exists()]
