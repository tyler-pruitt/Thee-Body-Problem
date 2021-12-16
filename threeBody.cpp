#include <iostream>
#include <string>
#include <math.h>
#include <vector>
#include <fstream>

using namespace std;

vector<vector<double>> eulerStep(vector<double> x, vector<double> y, vector<double> Vx, vector<double> Vy, vector<double> Ax, vector<double> Ay, double dt) {
    // Function takes in positions, velocities, accelerations, and dt as inputs
    // returns the newly calculated postions and velocities
    for (int i=0;i<3;i++) {
        x[i] += Vx[i] * dt;
        y[i] += Vy[i] * dt;

        Vx[i] += Ax[i] * dt;
        Vy[i] += Ay[i] * dt;
    }

    vector<vector<double>> outputs = {x, y, Vx, Vy};

    return outputs;
}

vector<vector<double>> computeAcceleration(vector<double> masses, vector<double> x, vector<double> y) {
    // Function takes in masses and initial positions as inputs
    // returns the instantaneous gravitational accelerations of each mass

    // Initialize the x and y distances between the three objects
    double x12 = x[1] - x[0];
    double x13 = x[2] - x[0];
    double x23 = x[1] - x[0];

    // Compute the distances between the objects
    double y12 = y[1] - y[0];
    double y13 = y[2] - y[0];
    double y23 = y[1] - y[0];

    double r12 = sqrt(pow(x12, 2) + pow(y12, 2));
    double r13 = sqrt(pow(x13, 2) + pow(y13, 2));
    double r23 = sqrt(pow(x23, 2) + pow(y23, 2));

    vector<double> Ax;
    vector<double> Ay;

    //  Compute the accelearations for object 1
    Ax.push_back(x12 * masses[1] / pow(r12, 3) + x13 * masses[2] / pow(r13, 3));
    Ay.push_back(y12 * masses[1] / pow(r12, 3) + y13 * masses[2] / pow(r13, 3));

    // Compute the accelearations for object 2
    Ax.push_back(-x12 * masses[0] / pow(r12, 3) + x23 * masses[2] / pow(r23, 3));
    Ay.push_back(-y12 * masses[0] / pow(r12, 3) + y23 * masses[2] / pow(r23, 3));

    // Compute the accelearations for object 3
    Ax.push_back(-x13 * masses[0] / pow(r13, 3) - x23 * masses[1] / pow(r23, 3));
    Ay.push_back(-y13 * masses[0] / pow(r13, 3) - y23 * masses[1] / pow(r23, 3));
    
    vector<vector<double>> A = {Ax, Ay};

    return A;
}

void write(vector<double> x, vector<double> y, ofstream &file) {
    vector<string> object = {"Sun", "Earth", "Moon"};
    for (int i=0;i<3;i++) {        
        cout << object[i] << ":" << x[i] << ", " << y[i] << endl;
        
        file << object[i] << ":" << x[i] << ", " << y[i] << endl;
    }
}

int main() {
    // Initialize starting conditions (masses, speeds, and positions)
    // Indices indicate ["Sun"], ["Earth"], ["Moon"]
    vector<double> masses = {3.0, 0.01, 0.0001};
    cout << "Enter the masses for Sun (3.0), Earth (0.01), Moon (0.0001): ";
    cin >> masses[0];
    cin >> masses[1];
    cin >> masses[2];
    
    vector<double> Vx = {0, 0, 0};
    cout << "Enter the 3 initial velocites for Vx (0, 0, 0): ";
    cin >> Vx[0];
    cin >> Vx[1];
    cin >> Vx[2];

    vector<double> Vy = {0, 0.5477, 0.6891};
    cout << "Enter the 3 initial velocites for Vy (0, 0.5477, 0.6891): ";
    cin >> Vy[0];
    cin >> Vy[1];
    cin >> Vy[2];

    vector<double> x = {0, 10, 10.5};
    cout << "Enter the 3 initial positions for x (0, 10, 10.5): ";
    cin >> x[0];
    cin >> x[1];
    cin >> x[2];

    vector<double> y = {0, 0, 0};
    cout << "Enter the 3 initial positions for y (0, 0, 0): ";
    cin >> y[0];
    cin >> y[1];
    cin >> y[2];

    vector<double> Ax;
    vector<double> Ay;

    // Initialize time and time step
    double t = 0;
    double dt = 0.0005;

    ofstream outStream;
    outStream.open("threeBodyProblem.txt");

    while (sqrt( pow(x[1] - x[2], 2)  + pow(y[1] - y[2], 2) ) <= 3 && t < 1000) {
        // Compute the accelerations at this time
        vector<vector<double>> A = computeAcceleration(masses, x, y);
        Ax = A[0];
        Ay = A[1];

        // Compute new positions and velocities
        vector<vector<double>> outputs = eulerStep(x, y, Vx, Vy, Ax, Ay, dt);
        x = outputs[0];
        y = outputs[1];
        Vx = outputs[2];
        Vy = outputs[3];

        // Loop over all possible quarter of a second times
        for (int i=0;i<=2000;i++) {
            // If t is very close to or equal to a quarter of a second time: simulate the dynamics
            if (abs(t - 0.25 * i) < 0.001) {
                write(x, y, outStream);
            }
        }

        t += dt;
    }

    outStream.close();

    return 0;
}

