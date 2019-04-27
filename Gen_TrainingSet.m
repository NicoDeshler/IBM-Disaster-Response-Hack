
% Google Maps image data directories.
satImgDir = fullfile('satImgs');
mapImgDir = fullfile('mapImgs');

% Instantiate image data store.
satImgs = imageDatastore(satImgDir);
mapImgs = imageDatastore(mapImgDir);

trainingSet_Size = numels(satImgs.Files);

% Generate Low/Med/High Disaster Rating Training Sets
for i = 1:trainingSet_Size
    sat_raw = imread(satImgs, i);
    map_raw = imread(mapImgs, i);
    
    nominal_sat_roads = Isolate_Roads(sat_raw, map_raw);
    
    set = mod(i,3);
    switch(set)
        case 0
        disaster_sat_roads = Gaussian_Noise(nominal_sat_roads, 'low');
        
        case 1
        disaster_sat_roads = Gaussian_Noise(nominal_sat_roads, 'med');
        
        case 2
        disaster_sat_roads = Gaussian_Noise(nominal_sat_roads, 'high');
    end
    disaster_impact = nominal_sat_roads - disaster_sat_roads;
    
    
    
        
end
    
    



function roads = Isolate_Roads(sat_raw, map_raw)
% Isolates Roads by applying a thresholded map view image mask on the
% satellite view image. 
road_binary = Road_Mask(map_raw);
roads = bsxfun(@times, sat_raw, cast(road_binary, 'like', sat_raw));
end

function mask = Road_Mask(map_raw)
% Generate road binary from Google Maps map view image.

% Extract the individual red, green, and blue color channels.
redChannel = map_raw(:, :, 1);
greenChannel = map_raw(:, :, 2);
blueChannel = map_raw(:, :, 3);

% Find white, where each color channel is more than 250
thresholdValue = 250;
mask = redChannel > thresholdValue & greenChannel > thresholdValue & blueChannel > thresholdValue;

end

% Add gaussian noise to the roads based on the disaster intensity
% classification.
function road_disaster = Gaussian_Noise(road_nominal, disaster_rating)
m = mean(road_nominal);

% Blur variance determined based on disaster level
switch (disaster_rating)
    case 'low'
        gauss_var = m/4;
    case 'med'
        gauss_var = m/2;
    case 'high'
        gauss_var = m;
end

% Apply gaussian noise to image
noise = imnoise(zeros(size(road_nominal)), 'gaussian', 1, gauss_var);
road_disaster = road_nominal.*noise;
end


function Crop_Icon(img)
    n = 50;
    img = img(1:end-n,:,:);
end





