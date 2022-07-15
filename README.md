### A comparative study on improving sound similarity maps with semantic metadata

This repository contains all data relating to the master thesis on sound similarity maps conducted at University Pompeu Fabra, Barcelona.
[Not yet published] The paper is accessible [here](www.google.com).

Further you can checkout the interface of the similarity maps on [GitHub Pages](https://lennartnicolas.github.io/smc-master-thesis/).

### Abstract

Searching and browsing appropriate sounds within large collections of audio samples
can be challenging for musicians and sound designers. Most commonly, list-based
search approaches are being used for displaying content for music production, however
several attempts have been made to improve user experience by projecting
sounds in a two dimensional map. These maps usually rely on dimensionality reduction
methods like PCA, UMAP or t-SNE to translate an audio embedding or
another high dimensional feature representation into a low dimensional latent space,
which typically involves a trade-off between the preservation of the global and local
structure of the data. Providing metadata or custom distance measures to the
algorithms can improve the clustering, which however requires correct labels and a
solid feature representation. In this work, we address this issue by including user
metadata for classification refinement of the audio to achieve an improved label
description and post-process the point positions of the projection with the help of
class probabilities. We conducted a comparative study of different map layouts to
understand the usefulness of the aforementioned method to improve sound similarity
projections. In our study we found that adding semantics in a hierarchical
manner and having a more concise local structure assist both sound searching and
explorational browsing.

