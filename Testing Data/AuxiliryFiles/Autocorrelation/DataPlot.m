% 1. Configurações Iniciais
ficheiro = 'Data_Top_Block_Recording3.bin'; % Ajuste o caminho se necessário
threshold = 0.8; % O valor do seu limiar no GNU Radio

% 2. Ler os dados binários (Float32 do GNU Radio)
fileID = fopen(ficheiro, 'r');
if fileID == -1
    error('Não foi possível abrir o ficheiro. Verifique o caminho.');
end
data = fread(fileID, 'float32');
fclose(fileID);

% 3. Encontrar o primeiro pacote (primeiro pico acima do threshold)
idx_detecao = find(data > threshold, 1);

if isempty(idx_detecao)
    disp('Nenhum pacote detetado com este threshold na gravação.');
else
    % 4. Isolar uma janela de 450 amostras à volta do pico (ex: 50 antes, 400 depois)
    inicio_janela = max(1, idx_detecao - 50);
    fim_janela = min(length(data), idx_detecao + 400);
    amostras_janela = data(inicio_janela:fim_janela);

    % Recalcular a posição da deteção dentro desta nova janela mais pequena
    idx_detecao_janela = find(amostras_janela > threshold, 1);

    % 5. Criar a Figura e fazer o Plot
    figure('Name', 'Deteção de Preâmbulo Wi-Fi', 'Color', 'w');
    plot(amostras_janela, 'k', 'LineWidth', 1.2); % Linha preta ('k')
    hold on;

    % Adicionar linha horizontal do Threshold
    yline(threshold, '--k', 'threshold', 'LabelHorizontalAlignment', 'right', 'LabelVerticalAlignment', 'bottom');

    % 6. Formatação do Gráfico
    xlabel('Sample Index', 'FontSize', 12);
    ylabel('Autocorrelation', 'FontSize', 12);
    ylim([-0.05 1.1]);
    xlim([0 length(amostras_janela)]);
    set(gca, 'FontSize', 11);
    box on;
    hold off;
end