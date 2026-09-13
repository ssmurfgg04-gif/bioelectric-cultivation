"""Minimal numpy MLP with manual backprop (no torch — keeps the science layer
runner-light). One hidden layer, tanh, regression (MSE) or classification
(log-softmax). Enough capacity for the bioelectric-state -> outcome decoder.
"""

from __future__ import annotations

import numpy as np


class MLP:
    def __init__(self, d_in: int, d_hidden: int, d_out: int, seed: int = 0,
                 classification: bool = False, lr: float = 0.05):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, (2.0 / (d_in + d_hidden)) ** 0.5, (d_in, d_hidden))
        self.b1 = np.zeros(d_hidden)
        self.W2 = rng.normal(0, (2.0 / (d_hidden + d_out)) ** 0.5, (d_hidden, d_out))
        self.b2 = np.zeros(d_out)
        self.clf = classification
        self.lr = lr

    def forward(self, X: np.ndarray):
        H = np.tanh(X @ self.W1 + self.b1)
        Z = H @ self.W2 + self.b2
        if self.clf:
            Z = Z - Z.max(axis=1, keepdims=True)
            P = np.exp(Z)
            P /= P.sum(axis=1, keepdims=True)
            return H, P
        return H, Z

    def predict(self, X: np.ndarray) -> np.ndarray:
        H, out = self.forward(X)
        return out

    def predict_class(self, X: np.ndarray) -> np.ndarray:
        assert self.clf
        return self.predict(X).argmax(axis=1)

    def loss(self, X: np.ndarray, Y: np.ndarray) -> float:
        _, out = self.forward(X)
        if self.clf:
            m = len(X)
            return float(-np.mean(np.log(out[np.arange(m), Y] + 1e-12)))
        return float(np.mean((out - Y) ** 2))

    def train(self, X: np.ndarray, Y: np.ndarray, epochs: int = 200,
              batch: int = 64, verbose: bool = False) -> list[float]:
        X = np.atleast_2d(np.asarray(X, float))
        Y = np.asarray(Y)
        m = len(X)
        losses = []
        for ep in range(epochs):
            perm = np.random.default_rng(ep).permutation(m)
            for s in range(0, m, batch):
                idx = perm[s: s + batch]
                xb, yb = X[idx], Y[idx]
                H, out = self.forward(xb)
                if self.clf:
                    dZ = out.copy()
                    dZ[np.arange(len(idx)), yb] -= 1.0
                    dZ /= len(idx)
                else:
                    dZ = 2.0 * (out - yb) / len(idx)
                dW2 = H.T @ dZ
                db2 = dZ.sum(axis=0)
                dH = dZ @ self.W2.T * (1 - H**2)
                dW1 = xb.T @ dH
                db1 = dH.sum(axis=0)
                self.W1 -= self.lr * dW1
                self.b1 -= self.lr * db1
                self.W2 -= self.lr * dW2
                self.b2 -= self.lr * db2
            if verbose and ep % 25 == 0:
                losses.append(self.loss(X, Y))
        return losses
