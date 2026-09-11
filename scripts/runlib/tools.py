"""Normalize completeness without inventing pagination support."""
def catalog_contract(*, only_published, truncated, has_more=False, supports_cursor=False, cursor=None):
    if truncated: return {'complete':False,'nextAction':'recover-truncated-output'}
    if not only_published: return {'complete':False,'nextAction':'verify-publication-status'}
    if has_more or cursor:
        if not supports_cursor or not cursor:return {'complete':False,'nextAction':'unsupported-pagination'}
        return {'complete':False,'nextAction':'next-page','cursor':cursor}
    return {'complete':True,'nextAction':'done'}
