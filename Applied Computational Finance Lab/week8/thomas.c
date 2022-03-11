/* Algoritmo de Thomas para sistemas tridiagonais 
 *
 * Uso: x = thomas(b, a, c, f)
 *
 * donde
 * 	b = diagonal inferior
 * 	a = diagonal central
 * 	c = diagonal superior
 * 	f = vector independiente
 */

#include "mex.h"


void thomas(double *b, double *a, double *c, double *f, int N, double *x) {
	double *u = (double*) malloc(N*sizeof(double));	/* alphas */
	/*
	 * Como no existen dependencias entre el vector v (beta) y el vector x (vector solución) podemos
	 * optimizar el espacio utilizando el mismo vector para ambos. Es importante cuando hablamos de N's grandes.
	 */
	double *v = x;	/* betas */
	double *y = (double*) malloc(N*sizeof(double));
	register int i;

	u[0] = a[0];
	for (i=0; i<N-1; i++) {
		v[i] = b[i] / u[i];
		u[i+1] = a[i+1] - v[i]*c[i];
	}

	y[0] = f[0];
	for (i=1; i<N; i++)
		y[i] = f[i] - v[i-1]*y[i-1];

	x[N-1] = y[N-1] / u[N-1];
	for (i=N-2; i >= 0; i--)
		x[i] = (y[i] - c[i]*x[i+1]) / u[i];

	free(u);
	free(y);
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
	double *b, *a, *c, *f, *x;

	mwSize N;
	
	N = mxGetN(prhs[1]); /* importante tomar prhs[1]=a, puesto que N es la dimension de a (diagonal central) */

	/* Resolución do sistema */
	b = mxGetPr(prhs[0]);
	a = mxGetPr(prhs[1]);
	c = mxGetPr(prhs[2]);
	f = mxGetPr(prhs[3]);

	plhs[0] = mxCreateDoubleMatrix(1, N, mxREAL);
	x = mxGetPr(plhs[0]);

	thomas(b, a, c, f, (int)N, x);
}
