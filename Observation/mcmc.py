import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import odlib_chaurasiya as od

# def normal_pdf(x, mu, sigma):
#     return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

# def metropolis_hastings(mu, sigma, n_iterations, x0, proposal_width):
#     x = x0
#     samples = []
    
#     for _ in range(n_iterations):
#         x_proposed = np.random.normal(x, proposal_width)
#         acceptance_ratio = min(1, normal_pdf(x_proposed, mu, sigma) / normal_pdf(x, mu, sigma))
        
#         if np.random.random() < acceptance_ratio:
#             x = x_proposed
        
#         samples.append(x)
    
#     return np.array(samples)

# Set parameters
mu, sigma = 0, 1
n_iterations = 10
x0 = 10
proposal_width = 0.5



# # Run MCMC



# resRA1.append(metropolis_hastings(raList[0], raSD[0], n_iterations, x0, proposal_width))
# resRA2.append(metropolis_hastings(raList[1], raSD[1], n_iterations, x0, proposal_width))
# resRA3.append(metropolis_hastings(raList[2], raSD[2], n_iterations, x0, proposal_width))
# resDec1.append(metropolis_hastings(raList[0], raSD[0], n_iterations, x0, proposal_width))
# resDec2.append(metropolis_hastings(raList[1], raSD[1], n_iterations, x0, proposal_width))
# resDec3.append(metropolis_hastings(raList[2], raSD[2], n_iterations, x0, proposal_width))

# 1. Trace Plot
# plt.figure(figsize=(12, 4))
# plt.plot(samples)
# plt.title('Trace Plot')
# plt.xlabel('Iteration')
# plt.ylabel('Value')
# plt.show()

# 2. Autocorrelation Plot
# plt.figure(figsize=(12, 4))
# plt.acorr(samples - np.mean(samples), maxlags=10)
# plt.title('Autocorrelation Plot')
# plt.xlabel('Lag')
# plt.ylabel('Autocorrelation')
# plt.show()

# 3. Histogram with Overlay
# plt.figure(figsize=(12, 4))
# plt.hist(samples, bins=50, density=True, alpha=0.7)
# x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
# plt.plot(x, normal_pdf(x, mu, sigma), 'r-', lw=2)
# plt.title('Histogram with True Distribution Overlay')
# plt.xlabel('Value')
# plt.ylabel('Density')
# plt.show()

# 4. Running Mean Plot
# plt.figure(figsize=(12, 4))
# cumulative_means = np.cumsum(samples) / (np.arange(n_iterations) + 1)
# plt.plot(cumulative_means)
# plt.title('Running Mean Plot')
# plt.xlabel('Iteration')
# plt.ylabel('Cumulative Mean')
# plt.show()

# 5. 2D Random Walk Plot (using first 1000 samples for clarity)
# samples_2d = metropolis_hastings(mu, sigma, 100, x0, proposal_width)
#for i in range(3):
    # plt.figure(figsize=(8, 8))
    # plt.plot(resDec1[:-1], resDec1[1:], 'b-', alpha=0.5)
    # plt.plot(resDec1[:-1], resDec1[1:], 'ro', alpha=0.5, markersize=2)
    # plt.title('2D Random Walk Plot')
    # plt.xlabel('X(t)')
    # plt.ylabel('X(t+1)')
    # plt.axis('equal')
    # plt.show()


#np.random.normal
#input list of length of 3 for ra and dec
#mean, std dev, just input lists bruv

#6-23 7:34
#7-8 3:08
#7-13 7:06

resRA1 = []
resDec1 = []
resRA2 = []
resDec2 = []
resRA3 = []
resDec3 = []

raList = [od.convert_hms_to_sec(20, 2, 17.6)/3600, (od.convert_hms_to_sec(19, 48, 57.543))/3600, (od.convert_hms_to_sec(19, 43, 26.49))/3600]
decList = [od.convert_dms_to_sec(19, 22, 16.25)/3600, (od.convert_dms_to_sec(19, 27, 25.07))/3600, (od.convert_dms_to_sec(19, 4, 09.44))/3600]

raSD = [0.3788657604218315/3600, 0.07519353009683982/3600, 0.019875680186487443/3600]
decSD = [0.3336519673283078/3600, 0.07916573787554171/3600, 0.08989177283496019/3600]

# for i in range(10):
#     resRA[i] = np.random.normal