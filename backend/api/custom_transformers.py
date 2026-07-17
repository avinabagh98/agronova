from sklearn.base import BaseEstimator, TransformerMixin

class SkipTransformer(BaseEstimator, TransformerMixin):
    """Transformer that passes data through unchanged"""
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X

class Passthrough(BaseEstimator, TransformerMixin):
    """Passthrough transformer for pipeline compatibility"""
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X
