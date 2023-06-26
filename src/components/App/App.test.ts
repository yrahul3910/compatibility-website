import { screen } from '@testing-library/react';
import setup from '../../testUtils';

it('displays a form component', () => {
    setup('/');
    const link = screen.findAllByLabelText('form');
    expect(link).toBeInTheDocument();
});
